# โครงเว้น 30% — มีบางส่วนเว้นไว้ให้คุณเติมเอง
# เฉลย: starter/s1_moving_box.py · ใบ้: ในใบงาน session
#
# s1_moving_box.py  (คาบ 2 · Phase A · S1)
# Hello hardware: สี่เหลี่ยม (Box) ที่ขยับตามจอย และไม่หลุดจอ
#
# อันนี้เป็นก้าวแรกของคอร์ส: เราคุมของบนจอได้ด้วยมือของเราเอง
# ทักษะ 4 อย่างที่เราจะใช้ซ้ำในทุกเกม:  start() · Box · keys() · run()
#
# วิธีรัน: เปิดไฟล์นี้ใน BENTO IDE แล้วกดปุ่ม Program to Device
# หรือเซฟเป็น main.py แล้วรีเซ็ตบอร์ด
# กด Back บนจอยเพื่อออกกลับ Playground · กด Start เพื่อเริ่มเกมใหม่

import bentogame as game

game.title("MOVE BOX")                        # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

# สร้างสี่เหลี่ยมตัวแรก: x, y, กว้าง, สูง, สี
hero = game.Box(380, 180, 40, 40, game.CYAN)

BASE_SPEED = 6      # ความเร็วเริ่มต้น (พิกเซลต่อเฟรม) ตอนเพิ่งแตะจอย
MAX_SPEED  = 30     # ความเร็วสูงสุดเมื่อกดค้างนานพอ
hold_frames = 0     # กดค้างมากี่เฟรมแล้ว (ยิ่งมาก ยิ่งเร็ว)


def update():
    global hold_frames
    pressed = game.keys()                       # อ่านจอยเฟรมนี้

    # ============ ----- เติมส่วนนี้เอง (งานของคุณ): ขยับ hero ตามจอย ----- ============
    # อ่านปุ่มจาก pressed (ได้จาก game.keys() — ดู bentogame.py:262)
    # ขยับด้วยเมท็อด .move(dx, dy) ของ game.Box (bentogame.py:194)
    #
    # STEP 1: ดูว่าเฟรมนี้มีการกดทิศใดทิศหนึ่งไหม
    #         (pressed.left / pressed.right / pressed.up / pressed.down)
    #         ถ้ากดอยู่ ให้สะสม hold_frames (+= 1) · ถ้าไม่กดเลย รีเซ็ต hold_frames = 0
    #         แนวคิด: กดค้างนาน = ยิ่งวิ่งเร็ว
    # STEP 2: คำนวณ speed จาก BASE_SPEED, hold_frames และคุมเพดานด้วย MAX_SPEED
    #         (ลองใช้ min() เพื่อไม่ให้เกิน MAX_SPEED — สูตรคิดเอง / ดู starter ถ้าติด)
    # STEP 3: เรียก hero.move(...) ทีละทิศ
    #         ซ้าย/ขวา = ขยับแกน x · ขึ้น/ลง = ขยับแกน y
    #         ขึ้นกับซ้ายใช้ค่าลบ · ลงกับขวาใช้ค่าบวก
    # หมายเหตุ: hero.move() กัน "หลุดจอ" ให้อัตโนมัติ (clamp ขอบ) — ไม่ต้องเช็คขอบเอง
    #          Back = ออก · Start = เริ่มใหม่ — game.run() จัดการให้ก่อนถึง update()
       # <- ลบ pass ออกเมื่อเริ่มเขียน
    # ====================================================


    if pressed.left or pressed.right or pressed.up or pressed.down:
        hold_frames += 1
    else:
        hold_frames = 0

    speed = BASE_SPEED + hold_frames
    current_speed = min(speed , MAX_SPEED)  #คุมเพดานด้วย MAX_SPEED เลือกตัวน้อยกว่า
    #print(current_speed)

    if pressed.left:
        hero.move(-current_speed, 0)
    if pressed.right:
        hero.move(current_speed, 0)
    if pressed.up:
        hero.move(0, -current_speed)
    if pressed.down:
        hero.move(0, current_speed)

    #วิ่งเฉียง 

game.run(update)                    # วิ่งทุกเฟรมจนกว่าจะ return False
