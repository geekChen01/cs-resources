## Makefile，书中已经给出了，所以这里也直接给出模板
TARGET=new_kernel_geekchen
KDIR=/lib/modules/$(shell uname -r)/build
PWD=$(shell pwd)
obj-m+=$(TARGET).o
default:
	make -C $(KDIR) M=$(PWD) modules
clean:
	make -C $(KDIR) M=$(PWD) clean            
## 由于Makefile直接给出了，所以为了检验你的知识，需要你在实验报告中详细解析这个Makefile每一行的具体作用       