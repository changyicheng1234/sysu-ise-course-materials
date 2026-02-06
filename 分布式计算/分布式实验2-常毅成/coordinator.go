package mr

import (
	"log"
	"net"
	"os"
	"net/rpc"
	"net/http"
	"sync"
	"time"
)

const (
	Idle int = iota
	InProgress
	Completed
)

const (
	Map int = iota
	Reduce
	Exit
	Wait
)

type Task struct {
	Input   string
	State   int
	Reducer int
	Num     int
	Temp    []string
	Output  string
}

type CoordinatorTask struct {
	Status     int
	StartTime  time.Time
	TaskDetail *Task
}

type Coordinator struct {
	Queue      chan *Task
	Info       map[int]*CoordinatorTask
	Co_status  int
	N_reduce   int
	File       []string
	TempFiles  [][]string
}

var mu sync.Mutex

// Your code here -- RPC handlers for the worker to call.

//
// an example RPC handler.
//
// the RPC argument and reply types are defined in rpc.go.
//
func (c *Coordinator) Example(args *ExampleArgs, reply *ExampleReply) error {
	reply.Y = args.X + 1
	return nil
}

//
// start a thread that listens for RPCs from worker.go
//
func (c *Coordinator) server() {
	rpc.Register(c)
	rpc.HandleHTTP()
	//l, e := net.Listen("tcp", ":1234")
	sockname := coordinatorSock()
	os.Remove(sockname)
	l, e := net.Listen("unix", sockname)
	if e != nil {
		log.Fatal("listen error:", e)
	}
	go http.Serve(l, nil)
}

//
// main/mrcoordinator.go calls Done() periodically to find out
// if the entire job has finished.
//
func (c *Coordinator) Done() bool {
	// ret := false

	// Your code here.
	mu.Lock()
	defer mu.Unlock()
	ret := (c.Co_status == Exit)
	time.Sleep(100 * time.Millisecond) // wait for Worker's exit
	return ret
}

func (c *Coordinator) allTaskDone() bool {
	for _, task := range c.Info {
		if task.Status != Completed {
			return false
		}
	}
	return true
}

//
// create a Coordinator.
// main/mrcoordinator.go calls this function.
// nReduce is the number of reduce tasks to use.
//
func MakeCoordinator(files []string, nReduce int) *Coordinator {
	c := Coordinator{
		Queue:     make(chan *Task, max(nReduce, len(files))),
		Info:      make(map[int]*CoordinatorTask),
		Co_status: Map,
		N_reduce:  nReduce,
		File:      files,
		TempFiles: make([][]string, nReduce),
	}
	c.mapTask()
	c.server()
	go c.catchTimeout()
	return &c
}

func (c *Coordinator) mapTask() {
	for idx, file_name := range c.File {
		taskMeta := Task{
			Input:   file_name,
			State:   Map,
			Reducer: c.N_reduce,
			Num:     idx,
		}
		c.Queue <- &taskMeta
		c.Info[idx] = &CoordinatorTask{
			Status:     Idle,
			TaskDetail: &taskMeta,
		}
	}
}

func (c *Coordinator) reduceTask() {
	c.Info = make(map[int]*CoordinatorTask)
	for idx, files := range c.TempFiles {
		taskMeta := Task{
			State:   Reduce,
			Reducer: c.N_reduce,
			Num:     idx,
			Temp:    files,
		}
		c.Queue <- &taskMeta
		c.Info[idx] = &CoordinatorTask{
			Status:     Idle,
			TaskDetail: &taskMeta,
		}
	}
}

func (c *Coordinator) catchTimeout() {
	for {
		time.Sleep(5 * time.Second)
		mu.Lock()
		if c.Co_status == Exit {
			mu.Unlock()
			return
		}
		for _, taskInfo := range c.Info {
			if taskInfo.Status == InProgress && time.Since(taskInfo.StartTime) > 20*time.Second {
				c.Queue <- taskInfo.TaskDetail
				taskInfo.Status = Idle
			}
		}
		mu.Unlock()
	}
}

func max(x int, y int) int {
	if x > y {
		return x
	}
	return y
}

