# โครงเว้น 30% — ช่องที่คุณต้องเติมเอง / เฉลยอยู่ที่ starter/catch.py
# ใบ้: ดูในใบงาน session ได้นะ
# catch.py — เกม "Catch" (MVP-1) สำหรับคาบ 3
# ตะกร้า (กล่อง) วิ่งซ้าย-ขวารับ "ของ" ที่ตกลงมา รับโดน = ได้แต้ม
# เล่นครบ 30 วินาที แล้วขึ้น GAME OVER + คะแนนรวม (เล่นจบเป็นรอบได้)
#
# รัน:  exec(open("catch.py").read())
# หยุด: กด Start บนจอย (หรือ Ctrl-C ที่ REPL)
#
# ใช้ API จาก starter/bentogame.py เท่านั้น — โครงเดียวกับ reference/pong_full.py
# (input -> move -> hit -> score -> จบด้วย return False)

import bentogame as game
import random

game.title("CATCH")                                              # หน้าเริ่ม: Start=เล่น  Back=ออก (title ทำ start ให้ในตัว)

# --- สร้าง Box / Text ครั้งเดียว (ห้ามสร้างใหม่ทุกเฟรม) ---
basket = game.Box(360, 360, 90, 20, game.GB_LIGHT)        # ตะกร้า อยู่ล่างจอ
item   = game.Box(380, 0, 24, 24, game.GB_LIGHTEST)       # ของ เริ่มบนสุด
score_text = game.Text("Score: 0", 10, 8, game.WHITE)     # ป้ายคะแนน มุมซ้ายบน

score  = 0
frames = 0
TOTAL  = 30 * 30          # 30 วินาที ที่ 30 fps = 900 เฟรม

BASE_SPEED = 6           # ความเร็วตะกร้าตอนเพิ่งแตะจอย
MAX_SPEED  = 30          # เร็วสูงสุดเมื่อกดค้างนานพอ
hold_frames = 0          # กดค้างมากี่เฟรมแล้ว (ยิ่งมาก ยิ่งเร็ว)


def update():
    global score, frames, hold_frames

    # --- คุมตะกร้าด้วยจอย: กดค้างยิ่งนานยิ่งเร็ว (move() clamp ขอบจออัตโนมัติ) ---
    pressed = game.keys()
    # ----- เติมส่วนนี้เอง (งานของคุณ): ขยับตะกร้าซ้าย-ขวาตามจอย -----
    # อ่านปุ่มจาก game.keys() ได้ค่ามาในตัวแปร pressed (มี .left / .right)
    # TODO:
    #   1) ถ้ากำลังกด left หรือ right อยู่ → เพิ่ม hold_frames ทีละ 1 ; ถ้าไม่ได้กด → รีเซ็ต hold_frames = 0
    if pressed.left or pressed.right:
        hold_frames += 1
    else:
        hold_frames = 0
    #   2) คำนวณ speed จาก BASE_SPEED + hold_frames แต่อย่าให้เกิน MAX_SPEED (ใช้ min())
    speed = BASE_SPEED + hold_frames
    current_speed = min(speed , MAX_SPEED)
    #   3) ถ้ากด left → เลื่อนตะกร้าไปทางลบ X ด้วย basket.move(...)
    #      ถ้ากด right → เลื่อนไปทางบวก X ด้วย basket.move(...)   (move() กันขอบจอให้เอง)
    if pressed.left:
        basket.move(-current_speed, 0)
    if pressed.right:
        basket.move(current_speed, 0)

    item.move_to(item.x, item.y+8)

    #ของหล่นลง
    if item.y > game.HEIGHT:
        item.move_to(random.randint(0, game.WIDTH - 24),0)

    if game.hit(basket, item):
        score += 1
        score_text.set(f"Score: {score}")
        game.sfx("eat")
        item.move_to(random.randint(0, game.WIDTH - 24),0)
    

    # --- จับเวลา 30 วินาที แล้วจบรอบ ---
    frames += 1

    if frames >= TOTAL:
        game.Text("GAME OVER",355 ,150 ,game.RED)
        game.Text(f"Score {score}",370 ,190 ,game.CYAN)
        game.sfx("gameover")
        
        return False

game.run(update, fps=30)
