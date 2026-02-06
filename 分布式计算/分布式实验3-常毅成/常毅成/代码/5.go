package main

import (
	"context"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

const (
	numTasks = 5       // 任务数量
	timeout  = 2 * time.Second // 超时时间
)

// 模拟一个任务函数，任务随机执行 1 到 5 秒钟
func task(id int, ctx context.Context, wg *sync.WaitGroup) {
	defer wg.Done()

	// 随机任务执行时间
	taskDuration := time.Duration(rand.Intn(5)+1) * time.Second
	fmt.Printf("Task %d started, will run for %v\n", id, taskDuration)

	select {
	case <-time.After(taskDuration): // 模拟任务执行完成
		fmt.Printf("Task %d completed\n", id)
	case <-ctx.Done(): // 如果context被取消或超时，提前终止任务
		fmt.Printf("Task %d cancelled: %v\n", id, ctx.Err())
	}
}

func main() {
	rand.Seed(time.Now().UnixNano()) // 随机数种子

	// 创建一个带超时的 context
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel() // 超时后自动取消所有任务

	var wg sync.WaitGroup

	// 启动多个任务
	for i := 1; i <= numTasks; i++ {
		wg.Add(1)
		go task(i, ctx, &wg)
	}

	// 等待所有任务完成或者超时
	wg.Wait()

	// 输出最终信息
	if ctx.Err() == context.DeadlineExceeded {
		fmt.Println("Timed out: Not all tasks completed in time.")
	} else {
		fmt.Println("All tasks completed successfully.")
	}
}

