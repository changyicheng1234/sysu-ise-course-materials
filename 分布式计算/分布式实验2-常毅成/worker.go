package mr

import (
	"fmt"
	"log"
	"net/rpc"
	"hash/fnv"
	"encoding/json"
	"io/ioutil"
	"os"
	"path/filepath"
	"sort"
	"time"
)

type KeyValue struct {
	Key   string
	Value string
}

func ihash(key string) int {
	h := fnv.New32a()
	h.Write([]byte(key))
	return int(h.Sum32() & 0x7fffffff)
}

type ByKey []KeyValue

func (a ByKey) Len() int           { return len(a) }
func (a ByKey) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByKey) Less(i, j int) bool { return a[i].Key < a[j].Key }

//
// main/mrworker.go calls this function.
//
func Worker(mapf func(string, string) []KeyValue, reducef func(string, []string) string) {

	// Your worker implementation here.

	for { // ask for task constantly
		task := getTask()
		switch task.State { // an action for a type
		case Map:
			mapper(&task, mapf)
		case Reduce:
			Reducer(&task, reducef)
		case Wait:
			time.Sleep(time.Second)
		case Exit:
			return
		default: // if no match
			time.Sleep(time.Second)
			continue
		}
	}
	// uncomment to send the Example RPC to the coordinator.
	// CallExample()

}
func call(rpcname string, args interface{}, reply interface{}) bool {
	// c, err := rpc.DialHTTP("tcp", "127.0.0.1"+":1234")
	sockname := coordinatorSock()
	c, err := rpc.DialHTTP("unix", sockname)
	if err != nil {
		log.Fatal("dialing:", err)
	}
	defer c.Close()
	err = c.Call(rpcname, args, reply)
	if err == nil {
		return true
	}
	fmt.Println(err)
	return false
}
func mapper(task *Task, mapf func(string, string) []KeyValue) {
	content, err := ioutil.ReadFile(task.Input) // read content
	if err != nil {
		log.Fatal("Fail to read file: " + task.Input, err)
	}
	intermediateKVs := mapf(task.Input, string(content)) // map task
	buffer := make([][]KeyValue, task.Reducer)           // divide into N_reduce parts
	for _, kv := range intermediateKVs {
		slot := ihash(kv.Key) % task.Reducer
		buffer[slot] = append(buffer[slot], kv)
	}
	tempFiles := make([]string, 0)
	for i := 0; i < task.Reducer; i++ {
		tempFiles = append(tempFiles, writeIntermediateFile(task.Num, i, &buffer[i]))
	}
	task.Temp = tempFiles // get location
	TaskCompleted(task)   // task completed
}

func Reducer(task *Task, reducef func(string, []string) string) {
	intermediateData := *readIntermediateFiles(task.Temp) // get location
	sort.Sort(ByKey(intermediateData))
	dir, _ := os.Getwd()
	tempFile, err := ioutil.TempFile(dir, "mr-tmp-*")
	if err != nil {
		log.Fatal("Failed to create temp file", err)
	}
	i := 0
	for i < len(intermediateData) { // partly from mrsequential.go
		j := i + 1
		for j < len(intermediateData) && intermediateData[j].Key == intermediateData[i].Key {
			j++
		}
		values := []string{}
		for k := i; k < j; k++ {
			values = append(values, intermediateData[k].Value)
		}
		outputValue := reducef(intermediateData[i].Key, values) // reduce task
		fmt.Fprintf(tempFile, "%v %v\n", intermediateData[i].Key, outputValue)
		i = j
	}
	tempFile.Close()
	outputFileName := fmt.Sprintf("mr-out-%d", task.Num)
	os.Rename(tempFile.Name(), outputFileName)
	task.Output = outputFileName
	TaskCompleted(task)
}

func writeIntermediateFile(mapID int, reduceID int, kvs *[]KeyValue) string {
	dir, _ := os.Getwd()
	tempFile, err := ioutil.TempFile(dir, "mr-tmp-*")
	if err != nil {
		log.Fatal("Failed to create temp file", err)
	}
	enc := json.NewEncoder(tempFile)
	for _, kv := range *kvs {
		if err := enc.Encode(&kv); err != nil {
			log.Fatal("Failed to write key-value pair", err)
		}
	}
	tempFile.Close()
	outputName := fmt.Sprintf("mr-%d-%d", mapID, reduceID)
	os.Rename(tempFile.Name(), outputName)
	return filepath.Join(dir, outputName)
}

func readIntermediateFiles(filePaths []string) *[]KeyValue {
	intermediateKVs := []KeyValue{}
	for _, filePath := range filePaths {
		file, err := os.Open(filePath)
		if err != nil {
			log.Fatal("Failed to open file "+filePath, err)
		}
		decoder := json.NewDecoder(file)
		for {
			var kv KeyValue
			if err := decoder.Decode(&kv); err != nil {
				break
			}
			intermediateKVs = append(intermediateKVs, kv)
		}
		file.Close()
	}
	return &intermediateKVs
}

