import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {
pg.K_UP: (0, -5),
pg.K_DOWN: (0, +5),
pg.K_LEFT: (-5, 0),
pg.K_RIGHT: (+5, 0),
}

accs = [a for a in range(1, 11)]


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内　OR 画面外を判定し、真理値タプルを返す関数
    引数:rct:効果トンor爆弾surfaceのRect
    戻り値:横方向・縦方向の真理値タプル（True：画面内／False：画面外）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
        
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/utyu.jpeg")
    kk_img = pg.image.load("ex02/fig/anapan.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 200, 200 
    bb_img = pg.image.load("ex02/fig/baikin.png")
    #bb_img = pg.Surface((20,20))
    #bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img,(0, 0, 0),(10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    accs = [a for a in range(1, 11)]
    clock = pg.time.Clock()
    tmr = 0
    
    kk_zis = { #演習１
    (5, 0):pg.transform.rotozoom(kk_img, 0, 1.0),
    (5,-5):pg.transform.rotozoom(kk_img, 316, 1.0),
    (0,-5):pg.transform.rotozoom(kk_img, 270, 1.0),
    (-5,-5):pg.transform.rotozoom(kk_img, 315, 1.0),
    (-5,0):pg.transform.rotozoom(kk_img, 0, 1.0),
    (-5,5):pg.transform.rotozoom(kk_img, 45, 1.0),
    (0, 5):pg.transform.rotozoom(kk_img, 90, 1.0),
    (5, 5):pg.transform.rotozoom(kk_img, 45, 1.0),
    }
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bb_rct):
            
            print("Game Over")
            return
            
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]: #キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
                
        if(sum_mv[0] >= 5):#演習１
            kk_img = pg.transform.flip(kk_img,False, True)
        if sum_mv != [0, 0]:
            kk_img = kk_zis[tuple(sum_mv)]
            if sum_mv[0] >= 5:
                kk_img = pg.transform.flip(kk_img, True, False)
                

                
        
                
    
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct) 
        
        
            
        if not yoko: #横方向にはみ出たら
            vx *= -1
        if not tate:#縦方向にはみ出たら
            vy *= -1
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        
        
        clock.tick(40)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()