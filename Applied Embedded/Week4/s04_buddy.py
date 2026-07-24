# ของห้ามรับ — item สีแดงที่รับแล้ว score -= 2 — เก็บ &quot;ชนิด&quot; ไว้ในตัวแปรคู่กับ item แล้วเช็กตอน game.hit เป็นจริง โดยไม่เพิ่ม Box เกินจำเป็น
import bentogame as game
import random

game.title("CATCH")                                              # หน้าเริ่ม: Start=เล่น  Back=ออก (title ทำ start ให้ในตัว)

# --- สร้าง Box / Text ครั้งเดียว (ห้ามสร้างใหม่ทุกเฟรม) ---
basket = game.Box(360, 360, 90, 20, game.GB_LIGHT)        # ตะกร้า อยู่ล่างจอ
item   = game.Box(380, 0, 24, 24, game.GB_LIGHTEST)       # ของ เริ่มบนสุด
score_text = game.Text("Score: 0", 10, 8, game.WHITE)     # ป้ายคะแนน มุมซ้ายบน
time_text  = game.Text("Time 0", 700, 50, game.CYAN)

score  = 0
frames = 0
TOTAL  = 30 * 30          # 30 วินาที ที่ 30 fps = 900 เฟรม

BASE_SPEED = 6           # ความเร็วตะกร้าตอนเพิ่งแตะจอย
MAX_SPEED  = 30          # เร็วสูงสุดเมื่อกดค้างนานพอ
hold_frames = 0          # กดค้างมากี่เฟรมแล้ว (ยิ่งมาก ยิ่งเร็ว)

kind = "normal"
def respawn():         #สุ่มว่าเป็นอันไหน
    global kind
    
    kind = random.choice(["normal", "red"]) 
    
    item.set_color(game.RED if kind == "red" else game.GB_LIGHTEST)
    
    item.move_to(random.randint(0, game.WIDTH - 24),0) #รีเซ็ตไปข้างบน
    

def update():
    global score, frames, hold_frames,kind
    # --- คุมตะกร้าด้วยจอย: กดค้างยิ่งนานยิ่งเร็ว (move() clamp ขอบจออัตโนมัติ) ---
    pressed = game.keys()

    if pressed.left or pressed.right:
        hold_frames += 2
    else:
        hold_frames = 0


    speed = BASE_SPEED + hold_frames
    current_speed = min(speed , MAX_SPEED)

    if pressed.left:
        basket.move(-current_speed, 0)
    if pressed.right:
        basket.move(current_speed, 0)





    #สุ่มระหว่าง ฟ้า กับ แดง
    #ของหล่นลง

    
    item.move_to(item.x, item.y+14)
    
    if item.y > game.HEIGHT:
    
        item.move_to(random.randint(0, game.WIDTH - 24),0)

        respawn()

    if game.hit(basket, item):
        
        if kind == "normal": #โดนสีปกติ
            score += 1
            game.sfx("eat")   
        elif kind == "red":     #โดนสีแดง
            score -= 2
            game.sfx("hit")

            
        score_text.set(f"Score: {score}")
        

       
        respawn()

    # --- จับเวลา 30 วินาที แล้วจบรอบ ---
    frames += 1
    time_text.set(f"Frame {frames}")


    
    if frames >= TOTAL:
        game.Text("GAME OVER",355 ,150 ,game.RED)
        game.Text(f"Score {score}",370 ,190 ,game.CYAN)
        game.sfx("gameover")
        
        return False

game.run(update, fps=30)
