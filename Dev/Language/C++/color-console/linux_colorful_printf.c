#include <stdio.h>
/*
#define DBG_PRINT(format, arg...)   do { fprintf(stdout,"%ld,%d,[flash_sn]--- "format"\n",\
                                                 get_current_time(),getpid(),## arg);} \
												 
*/											 
#define NONE                 "\e[0m"
#define BLACK                "\e[0;30m"
#define L_BLACK              "\e[1;30m"
#define RED                  "\e[0;31m"
#define L_RED                "\e[1;31m"
#define GREEN                "\e[0;32m"
#define L_GREEN              "\e[1;32m"
#define BROWN                "\e[0;33m"
#define YELLOW               "\e[1;33m"
#define BLUE                 "\e[0;34m"
#define L_BLUE               "\e[1;34m"
#define PURPLE               "\e[0;35m"
#define L_PURPLE             "\e[1;35m"
#define CYAN                 "\e[0;36m"
#define L_CYAN               "\e[1;36m"
#define GRAY                 "\e[0;37m"
#define WHITE                "\e[1;37m"
 
#define BOLD                 "\e[1m"
#define UNDERLINE            "\e[4m"
#define BLINK                "\e[5m"
#define REVERSE              "\e[7m"
#define HIDE                 "\e[8m"
#define CLEAR                "\e[2J"
#define CLRLINE              "\r\e[K" //or "\e[1K\r"
 
 
//#define NONE                 \e[0m
//#define RED                  \e[0;31m
#define printr(format, arg...) do{printf(RED format NONE,## arg);}while(0)
#define printg(format, arg...) do{printf(GREEN format NONE,## arg);}while(0)
#define printb(format, arg...) do{printf(BLUE format NONE,## arg);}while(0)
#define printk(format, arg...) do{printf(BLACK format NONE,## arg);}while(0)
#define printw(format, arg...) do{printf(WHITE format NONE,## arg);}while(0)
#define printy(format, arg...) do{printf(YELLOW format NONE,## arg);}while(0)
#define printc(format, arg...) do{printf(CYAN format NONE,## arg);}while(0)
#define printp(format, arg...) do{printf(PURPLE format NONE,## arg);}while(0)	
	
#define printlr(format, arg...) do{printf(L_RED format NONE,## arg);}while(0)
#define printlg(format, arg...) do{printf(L_GREEN format NONE,## arg);}while(0)
#define printlb(format, arg...) do{printf(L_BLUE format NONE,## arg);}while(0)
#define printlk(format, arg...) do{printf(L_BLACK format NONE,## arg);}while(0)
#define printlw(format, arg...) do{printf(L_WHITE format NONE,## arg);}while(0)
//#define printly(format, arg...) do{printf(L_YELLOW format NONE,## arg);}while(0)
#define printlc(format, arg...) do{printf(L_CYAN format NONE,## arg);}while(0)
#define printlp(format, arg...) do{printf(L_PURPLE format NONE,## arg);}while(0)	
int main()
{
	
	printf("普通字体\n");
	printr("红色字体\n");
	printg("绿色字体\n");
	printb("蓝色字体\n");
	printc("青色字体\n");
	printy("黄色字体\n");
	printp("粉色字体\n");
	
	printf("--普通字体\n");
	printlr("红色字体\n");
	printlg("绿色字体\n");
	printlb("蓝色字体\n");
	printlc("青色字体\n");
	//printly("黄色字体\n");
	printlp("粉色字体\n");
	return 0;
}
