package main

import (
    "fmt"
    "regexp"
    "strings"
)

func WordCount(text string) map[string]int {
    // 使用正则表达式去除标点符号
    re := regexp.MustCompile(`[^\w\s]`)
    cleanedText := re.ReplaceAllString(text, "")

    // 全部转换为小写，避免区分大小写
    cleanedText = strings.ToLower(cleanedText)

    // 按空格分割字符串为单词
    words := strings.Fields(cleanedText)

    // 创建一个map来存储单词出现的次数
    wordCount := make(map[string]int)

    // 统计每个单词的出现次数
    for _, word := range words {
        wordCount[word]++
    }

    return wordCount
}

func main() {
    text := "Hello, world! Hello!"
    result := WordCount(text)
    fmt.Println(result) // 输出: map[hello:2 world:1]
}

