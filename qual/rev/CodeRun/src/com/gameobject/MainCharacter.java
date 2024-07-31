package com.gameobject;

import java.applet.Applet;
import java.applet.AudioClip;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.URL;
import javax.imageio.ImageIO;

import com.util.Animation;

public class MainCharacter {

	public static final int LAND_POSY = 300;
	public static final float GRAVITY = 0.4f;
	
	private static final int NORMAL_RUN = 0;
	private static final int JUMPING = 1;
	private static final int DEATH = 2;
	
	private float posY;
	private float posX;
	private float speedX;
	private float speedY;
	private Rectangle rectBound;
	
	public int score = 0;
	
	private int state = NORMAL_RUN;
	
	private Animation normalRunAnim;
	private BufferedImage jumping;
	private BufferedImage deathImage;
	
	private AudioClip jumpSound;
	private AudioClip deadSound;
	private AudioClip scoreUpSound;
	
	public MainCharacter() {
		posX = 100;
		posY = LAND_POSY;
		rectBound = new Rectangle();
		normalRunAnim = new Animation(90);
		
		try {
			URL cd1 = MainCharacter.class.getResource("/com/data/code1.png");
			URL cd2 = MainCharacter.class.getResource("/com/data/code2.png");
			normalRunAnim.addFrame(ImageIO.read(cd1));
			normalRunAnim.addFrame(ImageIO.read(cd2));
			URL jmp =MainCharacter.class.getResource("/com/data/code-jump.png");
			jumping = ImageIO.read(jmp);
			URL dth =MainCharacter.class.getResource("/com/data/code-dead.png");
			deathImage = ImageIO.read(dth);

			URL js= MainCharacter.class.getResource("/com/data/jump.wav");
			jumpSound =  Applet.newAudioClip(js);
			URL ds= MainCharacter.class.getResource("/com/data/dead.wav");
			deadSound =  Applet.newAudioClip(ds);
			URL ss= MainCharacter.class.getResource("/com/data/scoreup.wav");
			scoreUpSound =  Applet.newAudioClip(ss);
		} catch (IOException e) {
            e.printStackTrace();
        }
		
	}

	public float getSpeedX() {
		return speedX;
	}

	public void setSpeedX(int speedX) {
		this.speedX = speedX;
	}
	
	public void draw(Graphics g) {
		switch(state) {
			case NORMAL_RUN:
				g.drawImage(normalRunAnim.getFrame(), (int) posX, (int) posY, null);
				break;
			case JUMPING:
				g.drawImage(jumping, (int) posX, (int) posY, null);
				break;
			case DEATH:
				g.drawImage(deathImage, (int) (posX+100), (int) (posY+50), null);
				break;
		}
	}
	
	public void update() {
		normalRunAnim.updateFrame();
		if(posY >= LAND_POSY) {
			posY = LAND_POSY;
			state = NORMAL_RUN;
		} else {
			speedY += GRAVITY;
			posY += speedY;
		}
	}
	
	public void jump() {
		if(posY >= LAND_POSY) {
			if(jumpSound != null) {
				jumpSound.play();
			}
			speedY = -10.5f;
			posY += speedY;
			state = JUMPING;
		}
	}
	
	
	public Rectangle getBound() {
		rectBound = new Rectangle();
		rectBound.x = (int) posX + 5;
		rectBound.y = (int) posY;
		rectBound.width = normalRunAnim.getFrame().getWidth() - 10;
		rectBound.height = normalRunAnim.getFrame().getHeight();
		return rectBound;
	}
	
	public void dead(boolean isDeath) {
		if(isDeath) {
			state = DEATH;
		} else {
			state = NORMAL_RUN;
		}
	}
	
	public void reset() {
		score=0;
		posY = LAND_POSY;
	}
	
	public void playDeadSound() {
		deadSound.play();
	}
	
	public void upScore() {
		score += 1;
		scoreUpSound.play();
	}
	
}
