package main

import (
	"fmt"
	"sync"
	"time"
)

type Counter struct {
	sync.RWMutex
	count int
}

// 读取计数器值
func (c *Counter) GetValue() int {
	c.RLock() // 使用读锁
	defer c.RUnlock()
	return c.count
}

// 增加计数器值
func (c *Counter) Increment() {
	c.Lock() // 使用写锁
	defer c.Unlock()
	c.count++
}

func reader(id int, counter *Counter, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < 5; i++ {
		value := counter.GetValue()
		fmt.Printf("Reader %d: Counter value = %d\n", id, value)
		time.Sleep(time.Millisecond * 200)
	}
}

func writer(id int, counter *Counter, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < 3; i++ {
		counter.Increment()
		fmt.Printf("Writer %d: Incremented counter\n", id)
		time.Sleep(time.Millisecond * 500)
	}
}

func main() {
	var counter Counter
	var wg sync.WaitGroup

	// 启动多个读取器
	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go reader(i, &counter, &wg)
	}

	// 启动多个写入器
	for i := 1; i <= 2; i++ {
		wg.Add(1)
		go writer(i, &counter, &wg)
	}

	// 等待所有goroutine完成
	wg.Wait()
}

