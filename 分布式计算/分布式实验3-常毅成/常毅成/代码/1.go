package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

const (
	numProducers = 3 // 生产者数量
	numConsumers = 3 // 消费者数量
	numItems      = 10 // 每个生产者生产的随机数个数
)

func producer(id int, ch chan int, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < numItems; i++ {
		num := rand.Intn(100)
		ch <- num
		fmt.Printf("Producer %d produced %d\n", id, num)
		time.Sleep(time.Millisecond * 500)
	}
}

func consumer(id int, ch chan int, wg *sync.WaitGroup) {
	defer wg.Done()
	for num := range ch { // 从通道中读取，直到通道关闭
		fmt.Printf("Consumer %d consumed %d\n", id, num)
		time.Sleep(time.Millisecond * 500)
	}
}

func main() {
	rand.Seed(time.Now().UnixNano())
	ch := make(chan int, 10)

	var producerWG sync.WaitGroup // 专门用于等待生产者
	var consumerWG sync.WaitGroup // 专门用于等待消费者

	// 启动生产者
	for i := 1; i <= numProducers; i++ {
		producerWG.Add(1)
		go producer(i, ch, &producerWG)
	}

	// 启动消费者
	for i := 1; i <= numConsumers; i++ {
		consumerWG.Add(1)
		go consumer(i, ch, &consumerWG)
	}

	// 等待所有生产者完成，然后关闭通道
	go func() {
		producerWG.Wait() // 等待所有生产者完成
		close(ch)         // 关闭通道，通知消费者结束
	}()

	consumerWG.Wait() // 等待所有消费者完成
}

