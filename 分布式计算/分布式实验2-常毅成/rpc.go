package mr

//
// RPC definitions.
//
// remember to capitalize all names.
//

import (
	"os"
	"strconv"
	"time"
)

//
// example to show how to declare the arguments
// and reply for an RPC.
//

type ExampleArgs struct {
	X int
}

type ExampleReply struct {
	Y int
}

func (c *Coordinator) GetTask(args *ExampleArgs, reply *Task) error { // coordinator call
	mu.Lock()
	defer mu.Unlock()
	if len(c.Queue) > 0 { // task exist
		*reply = *<-c.Queue
		c.Info[reply.Num].Status = InProgress
		c.Info[reply.Num].StartTime = time.Now()
	} else if c.Co_status == Exit { // coordinator is to exit
		*reply = Task{State: Exit}
	} else { // task doesn't exist temporarily
		*reply = Task{State: Wait}
	}
	return nil
}

func (c *Coordinator) TaskCompleted(task *Task, reply *ExampleReply) error { // coordinator call
	mu.Lock()
	defer mu.Unlock()
	if task.State != c.Co_status || c.Info[task.Num].Status == Completed { // update State
		return nil
	}
	c.Info[task.Num].Status = Completed
	go c.handleTaskCompletion(task)
	return nil
}

func (c *Coordinator) handleTaskCompletion(task *Task) { // coordinator call
	mu.Lock()
	defer mu.Unlock()
	switch task.State {
	case Map:
		for reduceTaskID, tempFilePath := range task.Temp { // get completed tasks' id and location
			c.TempFiles[reduceTaskID] = append(c.TempFiles[reduceTaskID], tempFilePath)
		}
		if c.allTaskDone() { // map -> reduce
			c.reduceTask()
			c.Co_status = Reduce
		}
	case Reduce:
		if c.allTaskDone() {
			c.Co_status = Exit
		}
	}
}

func getTask() Task { // worker call
	args := ExampleArgs{}
	reply := Task{}
	ok := call("Coordinator.GetTask", &args, &reply) // call
	if ok {
		// fmt.Printf("call succeeded!\n")
	} else {
		// fmt.Printf("call failed!\n")
	}
	return reply
}

func TaskCompleted(task *Task) { // worker call
	reply := ExampleReply{}
	call("Coordinator.TaskCompleted", task, &reply)
}

// Cook up a unique-ish UNIX-domain socket name
// in /var/Tmp, for the coordinator.
// Can't use the current directory since
// Athena AFS doesn't support UNIX-domain sockets.
func coordinatorSock() string {
	s := "/var/tmp/824-mr-"
	s += strconv.Itoa(os.Getuid())
	return s
}

