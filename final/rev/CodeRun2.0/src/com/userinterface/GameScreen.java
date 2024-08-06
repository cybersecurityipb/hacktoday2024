package com.userinterface;

import java.applet.Applet;
import java.applet.AudioClip;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.URL;
import java.math.BigInteger;
import java.awt.Font;

import javax.imageio.ImageIO;
import javax.swing.JPanel;

import com.gameobject.bugfly;
import com.gameobject.EnemiesManager;
import com.gameobject.GiftManager;
import com.gameobject.Land;
import com.gameobject.MainCharacter;

public class GameScreen extends JPanel implements Runnable, KeyListener {

	private static final int START_GAME_STATE = 0;
	private static final int GAME_PLAYING_STATE = 1;
	private static final int GAME_OVER_STATE = 2;
	private static final int GAME_FINISH = 3;
	private static final int GAME_LEVEL_UP = 4;
	
	private BigInteger targetlevel = new BigInteger("5");
	
	private Land land;
	private MainCharacter mainCharacter;
	private EnemiesManager enemiesManager;
	private bugfly bugfly;
	private Thread thread;
	private GiftManager gift;

	private boolean isKeyPressed;

	private int gameState = START_GAME_STATE;

	private BufferedImage gameOverButtonImage;
	private BufferedImage welcome;
	private BufferedImage finish;
	private BufferedImage levelup;
	private AudioClip music;

	public GameScreen() {
		mainCharacter = new MainCharacter();
		gift= new GiftManager();
		land = new Land(GameWindow.SCREEN_WIDTH, mainCharacter);
		mainCharacter.setSpeedX(4);
		try {
			URL go =MainCharacter.class.getResource("/com/data/gameover.png");
			gameOverButtonImage = ImageIO.read(go);
			URL wlc =MainCharacter.class.getResource("/com/data/welcome.png");
			welcome = ImageIO.read(wlc);
			URL fn =MainCharacter.class.getResource("/com/data/finish.png");
			finish = ImageIO.read(fn);
			URL lu =MainCharacter.class.getResource("/com/data/levelup.png");
			levelup = ImageIO.read(lu);

			URL backsoundpou= MainCharacter.class.getResource("/com/data/backsoundpou.wav");
			music =  Applet.newAudioClip(backsoundpou);
		} catch (IOException e) {
            e.printStackTrace();
        }

		enemiesManager = new EnemiesManager(mainCharacter);
		bugfly = new bugfly(GameWindow.SCREEN_WIDTH, mainCharacter);
	}

	public void startGame() {
		thread = new Thread(this);
		thread.start();
	}

	public void gameUpdate() {
		if (gameState == GAME_PLAYING_STATE) {
			bugfly.update();
			land.update();
			mainCharacter.update();
			enemiesManager.update();
			if (enemiesManager.isCollision()) {
				mainCharacter.playDeadSound();
				gameState = GAME_OVER_STATE;
				mainCharacter.dead(true);
			}else{
				if(mainCharacter.score.compareTo(targetlevel) == 0){
					gameState = GAME_LEVEL_UP;
					targetlevel = targetlevel.add(BigInteger.valueOf(5));
					mainCharacter.upLevel();
				}

				if(gift.verify(mainCharacter.level, mainCharacter.score)){
					gameState = GAME_FINISH;
				}
			}
		}
	}

	public void paint(Graphics g) {
		g.setColor(Color.decode("#394B59"));
		g.fillRect(0, 0, getWidth(), getHeight());

		switch (gameState) {
		case START_GAME_STATE:
			land.draw(g);
			mainCharacter.draw(g);
			g.drawImage(welcome, 270, 80, null);
			break;
		case GAME_PLAYING_STATE:
		case GAME_OVER_STATE:
			bugfly.draw(g);
			land.draw(g);
			enemiesManager.draw(g);
			mainCharacter.draw(g);

			g.setColor(Color.white);
			int fontSize = 14;
			Font font = new Font("Arial", Font.PLAIN, fontSize);
			g.setFont(font);
			g.drawString("SCORE: " + mainCharacter.score, 10, 450);
			g.drawString("LEVEL: " + mainCharacter.level, 10, 430);

			fontSize = 10;
			font = new Font("Arial", Font.PLAIN, fontSize);
			g.setFont(font);
			g.drawString("Copyright: backsound by Pou", 840, 450);
			if (gameState == GAME_OVER_STATE) {
				g.drawImage(gameOverButtonImage, 350, 150, null);	
				music.stop();		
			}
			break;
		case GAME_FINISH:
			
			g.drawImage(finish, 300, 0, null);
			g.setColor(Color.white);
			int fontSiz = 15;
			Font fon = new Font("Arial", Font.BOLD, fontSiz); 
			g.setFont(fon);
			
			g.drawString(gift.printgift(mainCharacter.level, mainCharacter.score), 140, 300);
			break;
		case GAME_LEVEL_UP:
			g.drawImage(levelup, 350, 150, null);
			g.setColor(Color.white);
			fontSiz = 40;
			fon = new Font("Arial", Font.PLAIN, fontSiz); 
			g.setFont(fon);
			
			g.drawString(mainCharacter.level+"", 480, 250);
			break;
		}
	}

	@Override
	public void run() {

		int fps = 100;
		long msPerFrame = 1000 * 1000000 / fps;
		long lastTime = 0;
		long elapsed;
		
		int msSleep;
		int nanoSleep;

		while (true) { 
			gameUpdate();
			repaint();
			if(gameState==GAME_FINISH) break;
			elapsed = (lastTime + msPerFrame - System.nanoTime());
			msSleep = (int) (elapsed / 1000000);
			nanoSleep = (int) (elapsed % 1000000);
			if (msSleep <= 0) {
				lastTime = System.nanoTime();
				continue;
			}
			try {
				Thread.sleep(msSleep, nanoSleep);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			lastTime = System.nanoTime();
		}
	}

	@Override
	public void keyPressed(KeyEvent e) {
		if (!isKeyPressed) {
			isKeyPressed = true;
			switch (gameState) {
			case START_GAME_STATE:
				music.loop();
				if (e.getKeyCode() == KeyEvent.VK_SPACE) {
					if(mainCharacter.level.compareTo(BigInteger.ONE) == 0)
						gameState = GAME_LEVEL_UP;
					else{
						gameState = GAME_PLAYING_STATE;
					}
				}
				break;
			case GAME_PLAYING_STATE:
				if (e.getKeyCode() == KeyEvent.VK_SPACE) {
					mainCharacter.jump();
				}
				break;
			case GAME_OVER_STATE:
				if (e.getKeyCode() == KeyEvent.VK_SPACE) {
					gameState = GAME_PLAYING_STATE;
					resetGame();
				}
				break;
			case GAME_LEVEL_UP:
				if (e.getKeyCode() == KeyEvent.VK_SPACE) {
					gameState = GAME_PLAYING_STATE;
					mainCharacter.reset();
				}
				break;
			}
		}
	}

	@Override
	public void keyReleased(KeyEvent e) {
		isKeyPressed = false;
	}

	@Override
	public void keyTyped(KeyEvent e) {
		//
	}

	private void resetGame() {
		music.loop();
		enemiesManager.reset();
		mainCharacter.dead(false);
		mainCharacter.reset();
	}

}
