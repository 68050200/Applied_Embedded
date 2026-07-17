#ไฟจราจรเดินเองตามเวลา - เปลี่ยนสีเองทุก 3 วินาที แต่กด USER BTN1 แล้วข้ามได้ทันที (ผสม "จำเวลาที่ผ่านไป" กับ edge detection — ทั้งเวลาและปุ่มต่างทำให้ transition เกิดได้)
# โดยทั้งสองต้องไม่ตีกัน

import gpio
import time

# ขอใช้ปุ่มดวงแรก (index 0 = SW1 บนบอร์ด) และไฟ LED 2 ดวงไว้บอกสถานะ
# ใช้ LED2 (เขียว) + RGB_RED — เลี่ยง LED1 (แดง, index 0) ที่ระบบหลักใช้
btn = gpio.button(0)
led_a = gpio.led(0)   # LED2 (เขียว)
led_b = gpio.led(1)   # RGB_RED
led_c = gpio.led(2)

# นิยาม state ของ FSM ให้อ่านง่าย แทนที่จะใช้ตัวเลขลอย ๆ
GREEN, YELLOW, RED = 0, 1, 2
state = GREEN

LED_PATTERN = {
    GREEN:  (False,  False, True), # ฟ้า แก้ไฟให้ตรง
    YELLOW: (False,  True, False), # เขียว
    RED:    (True, False, False), #แดง
}
NAME = {GREEN: "GREEN", YELLOW: "YELLOW", RED: "RED"}


def show(s):
    a_on, b_on, c_on= LED_PATTERN[s]
    # เติม: เปิด/ปิด led_a ตามค่า a_on  (ใช้ led_a.on() เมื่อ a_on เป็น True, ไม่งั้น led_a.off())
    if a_on == True:
        led_a.on()
    else:
        led_a.off()
    # เติม: เปิด/ปิด led_b ตามค่า b_on  (ใช้ led_b.on() / led_b.off())
    if b_on == True:
        led_b.on()
    else:
        led_b.off()
    if c_on == True:
         led_c.on()
    else:
        led_c.off()
    print("STATE =", NAME[s])

countdown_ms = 3000 #เปลี่ยนสีทุก 3 วิ

#ที่เปลี่ยนสี
def color_change():
    global state, change_state #ประกาศตัวแปร
    state = (state + 1) % 3
    show(state)
    change_state = time.ticks_ms() #เวลาที่เปลี่ยน = เวลาที่จับตอนนี้
# debounce: จำสถานะปุ่มรอบก่อน เพื่อจับ "ขอบขาลง" (กดลงครั้งเดียว)
# เติม: อ่านสถานะปุ่มปัจจุบันด้วย btn.is_pressed() มาเก็บไว้ใน prev_pressed
prev_pressed = btn.is_pressed()
#จับเวลาไปเรื่อยๆ
change_state = time.ticks_ms()

#prev_pressed = False
show(state)

print("กดปุ่ม BTN1(SW@) เพื่อเปลี่ยนไฟจราจร (Ctrl+C เพื่อหยุด)")
while True:
    pressed = btn.is_pressed()

    #กดปุ่ม
    if pressed and not prev_pressed: #<-edge detection 
        #รวบเปลี่ยนสีไปข้างบน
        color_change()
        time.sleep_ms(50)   # หน่วงสั้น ๆ ให้สัญญาณปุ่มนิ่งก่อนอ่านต่อ

    #เปลี่ยนออโต้
    #คำนวณหาความต่างของเวลาปัจจุบันกับตอนที่เปลี่ยนล่าสุด ว่าผ่านไปนาน >= countdown_ms(3 วิ) หรือ ไม่
    #แปลว่าเมื่อเวลาผ่านไป 3000 ms จะเข้าเงื่อนไข
    elif time.ticks_diff(time.ticks_ms(), change_state) >= countdown_ms:
        color_change()

    prev_pressed = pressed
    time.sleep_ms(10)       # คุมจังหวะ loop ไม่ให้ busy เกินจำเป็น
