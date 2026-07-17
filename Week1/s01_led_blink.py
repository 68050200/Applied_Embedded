# s01_led_blink.py - LED ดวงแรกของเรา (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) บนจอบอร์ด แตะเข้าเมนู Playground ก่อน
#          2) เติมช่องว่างตามคำใบ้ให้ครบ แล้วกด "Program to Device"
#          3) มองไฟ LED เล็ก ๆ ใต้จอ LCD — โชว์ทั้งหมดยาวประมาณ 2 นาที
#
# โมดูล gpio จัดการขา GPIO ที่ต่อกับ LED ให้เราเป็น output อยู่แล้ว
# แต่ละท่ากะพริบไม่เหมือนกัน เติมโค้ดให้ครบแล้วลองทายว่าต่างกันตรงไหน

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

# โชว์ 2 รอบ เผื่อรอบแรกยังหาไฟไม่เจอ รอบสองจะได้ดูทัน
for round_no in range(1, 3):
    print("=== รอบที่", round_no, "/ 2 ===")

    # --- ท่าที่ 1: กะพริบช้า วินาทีละครั้ง (10 ครั้ง ~ 10 วินาที) ---
    status.text("ท่า 1/5: กะพริบช้า (รอบ " + str(round_no) + "/2)")
    hint.text("ติดครึ่งวินาที ดับครึ่งวินาที ลองนับตามดู")
    print("ท่า 1: กะพริบช้า 1 Hz")
    for i in range(10):
        # เติม: สั่งให้ LED ติด ด้วย led.on()
        led.on()
        pass
        time.sleep_ms(500)
        # เติม: สั่งให้ LED ดับ ด้วย led.off()
        led.off()
        pass
        time.sleep_ms(500)

    # --- ท่าที่ 2: กะพริบเร็ว 5 เท่า (25 ครั้ง ~ 5 วินาที) ---
    # โค้ดเหมือนท่า 1 เป๊ะ เปลี่ยนแค่ตัวเลขเวลา — จังหวะเปลี่ยนทันที
    status.text("ท่า 2/5: กะพริบเร็ว")
    hint.text("โค้ดเดิม แค่ลด sleep_ms จาก 500 เหลือ 100")
    print("ท่า 2: กะพริบเร็ว 5 Hz")
    for i in range(25):
        # เติม: สลับสถานะ LED ด้วย led.toggle()  (ติด<->ดับ)
        led.toggle()
        pass
        time.sleep_ms(100)
    led.off()

    # --- ท่าที่ 3: จังหวะหัวใจเต้น ตุบ-ตุบ...พัก (8 ครั้ง ~ 10 วินาที) ---
    # จังหวะไม่จำเป็นต้องสม่ำเสมอ — สั้น สั้น แล้วเว้นยาว ก็เป็นภาษาแบบหนึ่ง
    status.text("ท่า 3/5: หัวใจเต้น ตุบ-ตุบ")
    hint.text("สองจังหวะติดกัน แล้วพักยาว เหมือนชีพจร")
    print("ท่า 3: heartbeat")
    for i in range(8):
        for beat in range(2):        # ตุบสองครั้งติดกัน
            led.on()
            time.sleep_ms(120)
            led.off()
            time.sleep_ms(120)
        # เติม: พักยาวหนึ่งช่วง ด้วย time.sleep_ms(700)
        time.sleep_ms(700)
        pass

    # --- ท่าที่ 4: รหัส SOS แบบมอร์ส (2 เที่ยว ~ 12 วินาที) ---
    # สั้นสามครั้ง = S, ยาวสามครั้ง = O, สั้นสามครั้ง = S
    # สังเกตว่า "ความยาวตอนติด" อยู่ในตัวแปร length_ms ที่วนจาก tuple
    status.text("ท่า 4/5: รหัส SOS")
    hint.text("สั้น 3 ยาว 3 สั้น 3 = ... --- ...")
    print("ท่า 4: SOS")
    for i in range(2):
        for length_ms in (150, 150, 150, 500, 500, 500, 150, 150, 150):
            led.on()
            # เติม: หน่วงเวลาตามค่า length_ms ด้วย time.sleep_ms(length_ms)
            time.sleep_ms(length_ms)
            pass
            led.off()
            time.sleep_ms(200)
        time.sleep_ms(800)           # เว้นก่อนส่งซ้ำ

    # --- ท่าที่ 5: ไฟวิ่ง knight-rider ข้าม LED ทุกดวง (~ 8 วินาที) ---
    status.text("ท่า 5/5: ไฟวิ่งข้ามทุกดวง")
    hint.text("คราวนี้มองให้ครบทุกดวง ไฟจะวิ่งไป-กลับ")
    print("ท่า 5: knight-rider")
    for sweep in range(6):
        # ไปข้างหน้า: 0, 1, 2, ...
        for i in range(n):
            # เติม: เปิด LED ดวงที่ i ด้วย gpio.led(i).on()
            gpio.led(i).on()
            pass
            time.sleep_ms(120)
            gpio.led(i).off()
        # ย้อนกลับ: ..., 2, 1 (ข้ามหัวท้ายกันจังหวะซ้ำ)
        for i in range(n - 2, 0, -1):
            gpio.led(i).on()
            time.sleep_ms(120)
            # เติม: ปิด LED ดวงที่ i ด้วย gpio.led(i).off()
            gpio.led(i).off()
            pass

# จบการแสดง เคลียร์ไฟให้ดับหมดทุกดวง
for i in range(n):
    gpio.led(i).off()

status.text("จบแล้ว เก่งมาก")
hint.text("ลองแก้ตัวเลข sleep_ms ในโค้ด แล้วกด Program ดูจังหวะใหม่")
print("จบแล้ว เก่งมาก ลองปรับเวลา sleep_ms ดูว่าจังหวะเปลี่ยนยังไง")
