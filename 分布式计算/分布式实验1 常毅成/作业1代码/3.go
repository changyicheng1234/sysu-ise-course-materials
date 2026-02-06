package main

import (
    "fmt"
)

func FindMaxKeyAndValue(m map[string]int) (string, int) {
    var maxKey string
    maxValue := -1 // 初始值设置为-1，假设值均为非负数

    for key, value := range m {
        // 找到更大的值或相同值但字母序更小的键
        if value > maxValue || (value == maxValue && key < maxKey) {
            maxValue = value
            maxKey = key
        }
    }

    return maxKey, maxValue
}

func main() {
    resultKey, resultValue := FindMaxKeyAndValue(map[string]int{"a": 10, "b": 20, "c": 20})
    fmt.Printf("Max Key: %s, Max Value: %d\n", resultKey, resultValue) // 输出: Max Key: b, Max Value: 20
}

