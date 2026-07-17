import gpio
import time
import ui

# ถามบอร์ดว่ามี LED กี่ดวง จะได้วนลูปไม่เกินจำนวนจริง
n = gpio.num_leds()
print("บอร์ดนี้มี LED ทั้งหมด", n, "ดวง")
print("ข้อมูลบอร์ด:", gpio.board_info())

# เตรียมหน้าจอ Playground: ล้างของเก่า แล้วปักป้ายบอกว่าให้มองตรงไหน
ui.clear()
ui.Label("มองไฟ LED เล็ก ๆ ใต้จอนี้", x=190, y=70, color=0xFFFFFF, value=28)
status = ui.Label("กำลังเริ่ม...", x=190, y=150, color=0x00FF88, value=24)
hint = ui.Label("", x=190, y=210, color=0xAAAAAA, value=20)

# ใช้ LED2 (เขียว, index 1) เพราะ LED1 (แดง, index 0) มักถูกใช้เป็นไฟ status
led = gpio.led(1)

# กำหนดแพทความเร็ว (ms)
ready = 1000
working = 5000
waiting = 1500
warning = 200
for round_no in range(1):
    status.text("สถานะ : พร้อม ")
    print("สถานะ : พร้อม")
    for i in range(5):
        led.on()
        time.sleep_ms(ready)
        led.off()
        time.sleep_ms(ready)

    status.text("สถานะ : ทำงาน ")
    print("สถานะ : ทำงาน")
    for i in range(1):
        led.on()
        time.sleep_ms(working)
        led.off()
        time.sleep_ms(100)

    status.text("สถานะ : รอ ")
    print("สถานะ : รอ")
    for i in range(5):
        led.on()
        time.sleep_ms(waiting)
        
        led.off()
        time.sleep_ms(waiting)

    status.text("สถานะ : เตือน ")
    print("สถานะ : เตือน")
    for i in range(5):
        led.on()
        time.sleep_ms(warning)
        
        led.off()
        time.sleep_ms(warning)

    status.text("สถานะ : พัง ")
    print("สถานะ : พัง")
    for i in range(1):
        led.off()
        time.sleep_ms(5000)

# จบการแสดง เคลียร์ไฟให้ดับหมดทุกดวง
for i in range(n):
    gpio.led(i).off()

status.text("End")
#hint.text("ลองแก้ตัวเลข sleep_ms ในโค้ด แล้วกด Program ดูจังหวะใหม่")
print("End")