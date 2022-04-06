


/////////////////////////////////////////////////////////
uint8_t clk   =14;//vfd clk
uint8_t din   =13;//vfd din
uint8_t cs    =15;//spi cs
uint8_t en    =16;//enable power of VFD module

unsigned char lightcmd;


#define NOP do { __asm__ __volatile__ ("nop"); } while (0)
#define ulong unsigned long 

void delay1();
void write_8bit(unsigned char w_data);
void VFD_cmd(unsigned char command);
void VFD_ALL_ON();
void VFD_show(void);
void VFD_init();
void VFD_WriteOneChar(unsigned char x, unsigned char chr);
void VFD_WriteStr(unsigned char x, char *str);
void VFD_Write_ADRAM(unsigned char ad_dat , unsigned char on_off_flag);
void VFDlightcmd(unsigned char lightcmd) ;



void delay1()
{ 
  for(ulong j=0;j<1000;j++) NOP;
}

void write_8bit(unsigned char w_data)
 { 
    unsigned char i;      
    for(i=0;i<8;i++)   
    {  
        digitalWrite(clk, LOW);    
        if( (w_data&0x01) == 0x01)       
      { 
           digitalWrite(din, HIGH);      
          }        
    else       
 { 
            digitalWrite(din, LOW);    
  } 
     w_data>>=1;  
     delay1();        
     digitalWrite(clk, HIGH);        
  }
 }  

void VFD_cmd(unsigned char command)
{
  digitalWrite(cs, LOW);
  write_8bit(command);
  digitalWrite(cs, HIGH);
  delay1();
}

void VFD_show(void)
{
  digitalWrite(cs, LOW);//开始传输
  write_8bit(0xe8);     //地址寄存器起始位置
  digitalWrite(cs, HIGH); //停止传输
}

void VFD_init()
{
  //SET HOW MANY digtal numbers
  digitalWrite(cs, LOW);
  write_8bit(0xe0);
  delay1();
  write_8bit(0x0B);//12 digtal
  digitalWrite(cs, HIGH);
  delay1();

  //set bright
  digitalWrite(cs, LOW);
  write_8bit(0xe4);
  delay1();
  write_8bit(0xFF);//leve 255 max
  digitalWrite(cs, HIGH);
  delay1();
}

void VFD_ALL_ON()
{
  digitalWrite(cs, LOW);
  write_8bit(0xe9);
  delay1();
}

/******************************
  在指定位置打印一个字符(用户自定义,所有CG-ROM中的)
  x:0~11;chr:要显示的字符编码
*******************************/
void VFD_WriteOneChar(unsigned char x, unsigned char chr)
{
  digitalWrite(cs, LOW);  //开始传输
  write_8bit(0x20 + x); //地址寄存器起始位置
  write_8bit(chr + 0x30);
  digitalWrite(cs, HIGH); //停止传输
  //VFD_show();
}
/******************************
  在指定位置打印字符串
  (仅适用于英文,标点,数字)
  x:0~11;str:要显示的字符串
*******************************/
void VFD_WriteStr(unsigned char x, char *str)
{
  digitalWrite(cs, LOW);  //开始传输
  write_8bit(0x20 + x); //地址寄存器起始位置
  while (*str)
  {
   //Serial.println(*str);
    write_8bit(*str); //ascii与对应字符表转换
    str++;
  }
  digitalWrite(cs, HIGH); //停止传输
 // VFD_show();
}

void VFD_Write_ADRAM(unsigned char ad_dat , unsigned char on_off_flag)
{
  unsigned char ad_dat_temp;
  digitalWrite(cs, LOW);  //开始传输 
  write_8bit(0x60 + ad_dat);  //ADRAM
  if(on_off_flag==1)//logo
  {write_8bit(0x02);}
  else if(on_off_flag==2)//just :
  {write_8bit(0x01);}
  else if(on_off_flag==3)//logo + :
  {write_8bit(0x03);}
  else if(on_off_flag==0)//nothing
  {write_8bit(0x00);}
  digitalWrite(cs, HIGH); //停止传输
  //VFD_show();
}



void VFDlightcmd(unsigned char lightcmd)  
 {  
  digitalWrite(cs, LOW);
  write_8bit(0xe4);
  delay1();
  write_8bit(lightcmd);//leve 255 max
  digitalWrite(cs, HIGH);
  delay1();
 } 







void setup() {
 
  Serial.begin(9600);
  pinMode(clk, OUTPUT);
  pinMode(din, OUTPUT);
  pinMode(cs, OUTPUT);
  pinMode(en, OUTPUT);

  Serial.println("pin set ok");
  digitalWrite(en, HIGH);//en=1,enable
  digitalWrite(cs, HIGH);
  
  VFD_init();
  VFD_ALL_ON();
  delay(1000);
  
  VFDlightcmd(0xf0); 
  VFD_WriteStr(0, "-LGL STUDIO-");
  VFD_show();
  delay(1000);

}


void loop() 
{ 
  
  unsigned char i; 
  for(i=10;i<255;i++)
  {
   VFD_WriteStr(0, "lightcmd:");
   VFD_WriteOneChar(9,i/100%100);
   VFD_WriteOneChar(10,i/10%10);
   VFD_WriteOneChar(11,i%10);
   VFDlightcmd(i); 
   VFD_show(); 
   delay(50);   
   }
  
  VFD_Write_ADRAM(0,1);
  VFD_Write_ADRAM(1,1);
  VFD_Write_ADRAM(2,1);
  VFD_Write_ADRAM(3,1);
  VFD_Write_ADRAM(4,1);
  VFD_Write_ADRAM(5,1);
  VFD_Write_ADRAM(6,1);
  VFD_Write_ADRAM(7,1);
  VFD_Write_ADRAM(8,0);
  VFD_Write_ADRAM(9,3);
  VFD_Write_ADRAM(10,3);
  VFD_Write_ADRAM(11,0);
  VFD_WriteOneChar(0,2);
  VFD_WriteOneChar(1,0);
  VFD_WriteOneChar(2,2);
  VFD_WriteOneChar(3,0);
  VFD_WriteOneChar(4,0);
  VFD_WriteOneChar(5,3);
  VFD_WriteOneChar(6,0);
  VFD_WriteOneChar(7,8);
  VFD_WriteOneChar(8,0);
  VFD_WriteOneChar(9,2);
  VFD_WriteOneChar(10,2);
  VFD_WriteOneChar(11,7);
  VFDlightcmd(0xff); 
  VFD_show();
  delay(1000);


  VFD_Write_ADRAM(0,1);
  VFD_Write_ADRAM(1,1);
  VFD_Write_ADRAM(2,1);
  VFD_Write_ADRAM(3,1);
  VFD_Write_ADRAM(4,1);
  VFD_Write_ADRAM(5,1);
  VFD_Write_ADRAM(6,1);
  VFD_Write_ADRAM(7,1);
  VFD_Write_ADRAM(8,1);
  VFD_Write_ADRAM(9,1);
  VFD_Write_ADRAM(10,1);
  VFD_Write_ADRAM(11,1);
  VFD_WriteStr(0, "ABCDEFGHIJKL");
  VFDlightcmd(40); 
  VFD_show();
  delay(1000);

  
}


