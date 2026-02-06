package main

import (
	"fmt"
)

// 定义 PersonalSalary 接口，包含 OutputInfo() 和 OutputWage() 方法
type PersonalSalary interface {
	OutputInfo()
	OutputWage()
}

// Staff 结构体，包含员工的基本信息
type Staff struct {
	num         string  // 编号
	name        string  // 姓名
	rateOfAttend float64 // 出勤率
	basicSal    float64 // 基本工资
	prize       float64 // 奖金
}

// Saleman 结构体，嵌套 Staff，并添加销售员的额外字段
type Saleman struct {
	Staff
	deductRate  float64 // 销售员提成比例
	personAmount float64 // 个人销售额
}

// Manager 结构体，嵌套 Staff，并添加经理的额外字段
type Manager struct {
	Staff
	totalDeductRate float64 // 经理提成比例
	totalAmount     float64 // 总销售额
}

// SaleManager 结构体，同时包含 Saleman 和 Manager 的字段
type SaleManager struct {
	Saleman
	Manager
}

// Staff 的 OutputInfo 方法实现，输出员工的基本信息
func (s Staff) OutputInfo() {
	fmt.Printf("编号: %s\n姓名: %s\n出勤率: %.1f\n基本工资: %.1f\n奖金: %.1f\n", 
		s.num, s.name, s.rateOfAttend, s.basicSal, s.prize)
}

// Staff 的 OutputWage 方法实现，计算并输出员工的实发工资
func (s Staff) OutputWage() {
	salary := s.basicSal + s.prize * s.rateOfAttend
	fmt.Printf("员工实发工资: %.1f\n", salary)
}

// Saleman 的 OutputInfo 方法实现，输出销售员的基本信息
func (s Saleman) OutputInfo() {
	s.Staff.OutputInfo()
	fmt.Printf("销售员提成比例: %.2f\n个人销售额: %.1f\n", s.deductRate, s.personAmount)
}

// Saleman 的 OutputWage 方法实现，计算并输出销售员的实发工资
func (s Saleman) OutputWage() {
	salary := s.basicSal + s.prize * s.rateOfAttend + s.personAmount * s.deductRate
	fmt.Printf("销售员实发工资: %.1f\n", salary)
}

// Manager 的 OutputInfo 方法实现，输出经理的基本信息
func (m Manager) OutputInfo() {
	m.Staff.OutputInfo()
	fmt.Printf("经理提成比例: %.2f\n经理总销售额: %.1f\n", m.totalDeductRate, m.totalAmount)
}

// Manager 的 OutputWage 方法实现，计算并输出经理的实发工资
func (m Manager) OutputWage() {
	salary := m.basicSal + m.prize * m.rateOfAttend + m.totalAmount * m.totalDeductRate
	fmt.Printf("经理实发工资: %.1f\n", salary)
}

// SaleManager 的 OutputInfo 方法实现，输出销售经理的全部信息
func (sm SaleManager) OutputInfo() {
	sm.Saleman.Staff.OutputInfo() // 显式调用 Saleman 的 Staff
	fmt.Printf("销售员提成比例: %.2f\n个人销售额: %.1f\n", sm.Saleman.deductRate, sm.Saleman.personAmount)
	fmt.Printf("经理提成比例: %.2f\n经理总销售额: %.1f\n", sm.Manager.totalDeductRate, sm.Manager.totalAmount)
}

// SaleManager 的 OutputWage 方法实现，计算并输出销售经理的实发工资
func (sm SaleManager) OutputWage() {
	// 使用 Saleman 和 Manager 的字段计算工资
	salary := sm.Saleman.basicSal + sm.Saleman.prize * sm.Saleman.rateOfAttend +
		sm.Saleman.personAmount * sm.Saleman.deductRate +
		sm.Manager.totalAmount * sm.Manager.totalDeductRate
	fmt.Printf("销售经理实发工资: %.1f\n", salary)
}

func main() {
	// 从图片中获取数据
	staff1 := Staff{"1", "s1", 0.6, 2000, 3000}
	staff2 := Staff{"2", "s2", 0.7, 3000, 4000}
	staff3 := Staff{"3", "s3", 0.5, 1000, 500}

	saleman1 := Saleman{staff1, 0.1, 8000}
	manager1 := Manager{staff2, 0.05, 9000}
	saleManager1 := SaleManager{Saleman: Saleman{staff3, 0.1, 8000}, Manager: Manager{staff3, 0.05, 9000}}

	// 输出信息和工资
	saleman1.OutputInfo()
	saleman1.OutputWage()
	fmt.Println("------------------------------------")
	manager1.OutputInfo()
	manager1.OutputWage()
	fmt.Println("------------------------------------")
	saleManager1.OutputInfo()
	saleManager1.OutputWage()
}

