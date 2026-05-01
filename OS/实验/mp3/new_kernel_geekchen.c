// 内核模块编程框架：
// 因为模块不与C函数库连接，所以不能包含通常的头文件，而且作为核心程序，只能使用内核函数
// 以下是与内核模块编程相关的
//
//c文件（模块程序）:头文件部分、初始化函数+清理函数+绑定函数入出口函数、模块许可申明。

//头文件部分
#include <linux/init.h>   // 含了一些在模块初始化和退出时使用的宏定义和函数, 例如__init和__exit宏
#include <linux/module.h>  // 定义了一些操作内核模块的函数，如module_init和module_exit/Needed by all modules */
#include <linux/kernel.h>  // 定义了一些用于打印调试信息和日志的函数，如pr_info、pr_warn和pr_err等/Needed for KERN_ALERT */

#include <linux/list.h>
#include <linux/sched.h>/*defined struct task_struct*/
#include <linux/init_task.h>

// 模块初始化函数
static int newmodule_init(void) {
    // 在模块加载时执行的初始化代码
    int num=0;
 	struct task_struct *p,*task;
//Linux内核的PCB是task_struct结构体，
//所有运行在系统中的进程都以task_struct链表的形式存在内核中

 	struct list_head *p1;
 	task = &init_task;
	printk("\t\t\tHello!\n");
	printk(KERN_ALERT"name\t\tpid\t\tstate\t\tfather_name\t\t");
	list_for_each(p1,&task->tasks)
 	{
 	p=list_entry(p1,struct task_struct,tasks);
	num=num+1;
	printk(KERN_ALERT"%s\t\t%d\t\t%d\t\t%d\t\t%s\t\t%d\n",p->comm,p->pid,p->__state,p->normal_prio,p->parent->comm,p->parent->pid);
 	}
    return 0;
}

// 模块退出函数
static void newmodule_exit(void) {
	printk(KERN_ALERT"Bye!\n");
    // 在模块卸载时执行的清理代码
}

// 注册模块初始化和退出函数 (函数注册)
module_init(newmodule_init);
module_exit(newmodule_exit);

// 模块附加信息(宏)
MODULE_AUTHOR("chen yusen");  
MODULE_DESCRIPTION("module of geek_chen");   // 简要地描述即可，use English.
MODULE_LICENSE("GPL");   // General Public License，这个不用改(模块许可申明)
MODULE_INFO(name, "masterpiece");
MODULE_INFO(version, "2.0");
MODULE_INFO(parm, "name=my_parameter1,type=int,mode=0644,default=0,description=My integer parameter");
//模块的参数列表，可以定义一些可配置的参数供用户调整模块行为。// 整型参数,默认值为 0，读写权限为可读可写：
MODULE_INFO(alias, "tasty_kernel");//模块的别名信息，用于指定其他名称引用该模块。

//...你还可以加一些其他地MODULE_xxx,比如MODULE_ALIAS等,自行STFW，上面三个是必须的
//我们会使用modinfo来识别你的内核模块的各种唯一标识性信息
