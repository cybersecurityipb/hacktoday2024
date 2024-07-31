package com.gameobject;

import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import javax.imageio.ImageIO;


public class EnemiesManager {
	
	private BufferedImage bug1;
	private BufferedImage bug2;
	private BufferedImage bug3;
	private BufferedImage bug4;
	private Random rand;
	
	private List<Enemy> enemies;
	private MainCharacter mainCharacter;
	
	public EnemiesManager(MainCharacter mainCharacter) {
		rand = new Random();
		try {
			URL b1 =MainCharacter.class.getResource("/com/data/bug1.png");
			bug1 = ImageIO.read(b1);
			URL b2 =MainCharacter.class.getResource("/com/data/bug2.png");
			bug2 = ImageIO.read(b2);
			URL b3 =MainCharacter.class.getResource("/com/data/bug3.png");
			bug3 = ImageIO.read(b3);
			URL b4 =MainCharacter.class.getResource("/com/data/bug4.png");
			bug4 = ImageIO.read(b4);
		} catch (IOException e) {
            e.printStackTrace();
        }
		enemies = new ArrayList<Enemy>();
		this.mainCharacter = mainCharacter;
		enemies.add(createEnemy());
	}
	
	public void update() {
		for(Enemy e : enemies) {
			e.update();
		}
		Enemy enemy = enemies.get(0);
		if(enemy.isOutOfScreen()) {
			mainCharacter.upScore();
			enemies.clear();
			enemies.add(createEnemy());
		}
	}
	
	public void draw(Graphics g) {
		for(Enemy e : enemies) {
			e.draw(g);
		}
	}
	
	private Enemy createEnemy() {
		// if (enemyType = getRandom)
		int type = rand.nextInt(4);
		if(type == 0) {
			return new bug(mainCharacter, 950, bug1.getWidth() - 10, bug1.getHeight() - 10, bug1);
		} else if(type==1){
			return new bug(mainCharacter, 950, bug2.getWidth() - 10, bug2.getHeight() - 10, bug2);
		}else if(type==2){
			return new bug(mainCharacter, 950, bug3.getWidth() - 10, bug3.getHeight() - 10, bug3);
		}else{
			return new bug(mainCharacter, 950, bug4.getWidth() - 10, bug4.getHeight() - 10, bug4);
		}
	}
	
	public boolean isCollision() {
		for(Enemy e : enemies) {
			if (mainCharacter.getBound().intersects(e.getBound())) {
				return true;
			}
		}
		return false;
	}
	
	public void reset() {
		enemies.clear();
		enemies.add(createEnemy());
	}
	
}
