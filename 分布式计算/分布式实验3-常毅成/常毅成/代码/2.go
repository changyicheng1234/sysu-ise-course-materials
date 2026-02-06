package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

const (
	numDataSources = 3    // 数据源数量
	dataCount      = 5    // 每个数据源发送的数据个数
)

func generateData(sourceID int, ch chan int, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < dataCount; i++ {
		data := rand.Intn(100) // 随机数据
		ch <- data
		fmt.Printf("DataSource %d produced %d\n", sourceID, data)
		time.Sleep(time.Millisecond * 500) // 模拟数据源产生数据的时间
	}
}

func main() {
	rand.Seed(time.Now().UnixNano())

	var wg sync.WaitGroup
	channels := make([]chan int, numDataSources) // 用于存放每个数据源的通道
	aggregateChannel := make(chan int)           // 聚合通道，用于收集所有数据源的结果

	// 启动多个数据源（goroutines）
	for i := 0; i < numDataSources; i++ {
		channels[i] = make(chan int)
		wg.Add(1)
		go generateData(i+1, channels[i], &wg)
	}

	// 启动一个goroutine来聚合数据
	go func() {
		wg.Wait()    // 等待所有数据源的生产者完成
		close(aggregateChannel) // 关闭聚合通道
	}()

	// 使用select从多个通道收集数据
	go func() {
		for {
			select {
			case data, ok := <-channels[0]:
				if ok {
					aggregateChannel <- data
				}
			case data, ok := <-channels[1]:
				if ok {
					aggregateChannel <- data
				}
			case data, ok := <-channels[2]:
				if ok {
					aggregateChannel <- data
				}
			}
		}
	}()

	// 从聚合通道收集最终结果
	go func() {
		for data := range aggregateChannel {
			fmt.Printf("Aggregated result: %d\n", data)
		}
	}()

	// 等待所有goroutine完成
	time.Sleep(time.Second * 5)
}

