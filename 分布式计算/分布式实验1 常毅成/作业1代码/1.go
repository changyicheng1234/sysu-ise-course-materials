package main
import "fmt"
// Rotate 旋转切片
func Rotate(slice []int, k int) []int {
    n := len(slice)
    k = k % n // 防止 k 超过 n
    // 反转整个切片
    reverse(slice, 0, n-1)
    // 反转前 k 个元素
    reverse(slice, 0, k-1)
    // 反转剩余的元素
    reverse(slice, k, n-1)
    
    return slice
}

// reverse 反转切片的一部分
func reverse(slice []int, start, end int) {
    for start < end {
        slice[start], slice[end] = slice[end], slice[start]
        start++
        end--
    }
}

func main() {
    arr := []int{1, 2, 3, 4, 5}
    k := 2
    result := Rotate(arr, k)
    fmt.Println(result) 
}

