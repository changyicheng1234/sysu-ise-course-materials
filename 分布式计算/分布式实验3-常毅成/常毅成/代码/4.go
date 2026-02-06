package main

import (
	"fmt"
	"sync"
)

func mapReduce(words []string) int {
	var wg sync.WaitGroup
	resultChannel := make(chan int, len(words)) // 使用缓冲通道来存储每个字符串的长度

	// 为每个字符串启动一个goroutine来计算其长度
	for _, word := range words {
		wg.Add(1)
		go func(w string) {
			defer wg.Done()
			resultChannel <- len(w) // 将字符串的长度发送到通道
		}(word)
	}

	// 等待所有goroutine完成
	wg.Wait()
	close(resultChannel)

	// 汇总所有结果
	totalLength := 0
	for length := range resultChannel {
		totalLength += length
	}

	return totalLength
}

func main() {
	words := []string{"Where", "did", "I", "put", "my", "lighter"}
	totalLength := mapReduce(words)
	fmt.Printf("Total length of all words: %d\n", totalLength)
}

