package com.gameobject;

import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Random;

import javax.imageio.ImageIO;

import com.userinterface.GameWindow;
import com.util.Animation;

public class bugfly {
	private List<ImageBug> listBug;
	private BufferedImage bugg;
	private Random rand;
	private Animation bugfly;
	private Animation bugfly2;
	
	private MainCharacter mainCharacter;
	
	
	public bugfly(int width, MainCharacter mainCharacter) {
		bugfly =new Animation(60);
		bugfly2 =new Animation(60);

		rand = new Random();
		this.mainCharacter = mainCharacter;
		try {  
			URL b1 =MainCharacter.class.getResource("/com/data/bugt1.png");
			URL b2 =MainCharacter.class.getResource("/com/data/bugt2.png");
			bugfly.addFrame(ImageIO.read(b1));
			bugfly.addFrame(ImageIO.read(b2));

			bugfly2.addFrame(ImageIO.read(b2));
			bugfly2.addFrame(ImageIO.read(b1));


			URL bug =MainCharacter.class.getResource("/com/data/bugt1.png");
			bugg  = ImageIO.read(bug);
		} catch (IOException e) {
            e.printStackTrace();
        }


		listBug = new ArrayList<ImageBug>();
		ImageBug imageBug = new ImageBug();

		for(int i=0;i<1000;i+=200){
			imageBug = new ImageBug();
			imageBug.posX = i;
			imageBug.posY = rand != null ? rand.nextInt(100) : 75;
			listBug.add(imageBug);
		}
	}
	
	public void update(){
		bugfly.updateFrame();
		bugfly2.updateFrame();
		Iterator<ImageBug> itr = listBug.iterator();
		ImageBug firstElement = itr.next();
		firstElement.posX -= mainCharacter.getSpeedX()/8;
		while(itr.hasNext()) {
			ImageBug element = itr.next();
			element.posX -= mainCharacter.getSpeedX()/8;
		}
		if(firstElement.posX < -bugg.getWidth()) {
			listBug.remove(firstElement);
			firstElement.posX = GameWindow.SCREEN_WIDTH;
			listBug.add(firstElement);
		}
	}
	
	public void draw(Graphics g) {
		for(ImageBug imgLand : listBug) {
			rand = new Random();
			int x=rand.nextInt(2);
			if(x==0){
				g.drawImage(bugfly.getFrame(), (int) imgLand.posX, imgLand.posY, null);
			}else{
				g.drawImage(bugfly2.getFrame(), (int) imgLand.posX, imgLand.posY, null);
			}
		}
	}
	
	private class ImageBug {
		float posX;
		int posY;
	}
}
