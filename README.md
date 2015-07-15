# Pong-clone
My first game- clone of Atari Pong


This is my first game.

Possible improvements:
 1. Use image instead of drawing grid( which is more intensive?)
 2. Create a list of points at the beginning and use lines() instead of line()
 3. Instead of divide , multiply with calculated val of 1/x - DONE
 4. Consider breaking program into multiple files. eg. config, logic, etc.. - DONE
 5. Ball doesn't even touch the paddle before bouncing. problem at high speed. find workaround. does it even exist
 6. Game becomes too slow, update only locations neccessary not entire screen
 7. Use self.rect = self.image.get_rect() instead of passing DISPLAYSURF - NOTNEEDED
 8. Consider breaking update into 2. handle event. then update. not handle event in update
 9. Use 2 render functions? is it worth it? one renders for the first time. the other is in pt 8
 10. Next project definitely use sprite class- will  make things simpler
 11. Very imp- simultaneous key input doesnt work. use get pressed instead? DONE
 12. Stop speed increase beyond a point. After a while, the ball becomes so fast, points are awarded for no reason
    
