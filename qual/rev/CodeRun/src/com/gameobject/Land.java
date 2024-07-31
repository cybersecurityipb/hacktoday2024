package com.gameobject;

import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javax.imageio.ImageIO;


public class Land {
	
	public static final int LAND_POSY = 405;
	
	private List<ImageLand> listLand;
	private BufferedImage land;
	
	private MainCharacter mainCharacter;
	
	public Land(int width, MainCharacter mainCharacter) {
		this.mainCharacter = mainCharacter;

		try {
			URL l1 =MainCharacter.class.getResource("/com/data/land1.png");
			land = ImageIO.read(l1);
		} catch (IOException e) {
            e.printStackTrace();
        }

		int numberOfImageLand = width / land.getWidth() + 2;
		listLand = new ArrayList<ImageLand>();
		for(int i = 0; i < numberOfImageLand; i++) {
			ImageLand imageLand = new ImageLand();
			imageLand.posX = i * land.getWidth();
			setImageLand(imageLand);
			listLand.add(imageLand);
		}
	}
	
	public void update(){
		Iterator<ImageLand> itr = listLand.iterator();
		ImageLand firstElement = itr.next();
		firstElement.posX -= mainCharacter.getSpeedX();
		float previousPosX = firstElement.posX;
		while(itr.hasNext()) {
			ImageLand element = itr.next();
			element.posX = previousPosX + land.getWidth();
			previousPosX = element.posX;
		}
		if(firstElement.posX < -land.getWidth()) {
			listLand.remove(firstElement);
			firstElement.posX = previousPosX + land.getWidth();
			setImageLand(firstElement);
			listLand.add(firstElement);
		}
	}
	
	private void setImageLand(ImageLand imgLand) {
		imgLand.image = land;
	}
	
	public void draw(Graphics g) {
		for(ImageLand imgLand : listLand) {
			g.drawImage(imgLand.image, (int) imgLand.posX, LAND_POSY, null);
		}
	}
	
	private class ImageLand {
		float posX;
		BufferedImage image;
	}
	
}
