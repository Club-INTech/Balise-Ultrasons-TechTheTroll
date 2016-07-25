package balise;

import javax.imageio.ImageIO;
import javax.swing.*;

import filtres.Vec2;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Interface graphique écrite à l'arrache
 * @author pf
 *
 */

public class Display extends JPanel {

	private class Point
	{
		public int x, y;
		Couleur couleur;
		
		public Point(int x, int y, Couleur couleur)
		{
			this.x = x;
			this.y = y;
			this.couleur = couleur;
		}

		public Point(Vec2 p, Couleur couleur)
		{
			this((int)p.x, (int)p.y, couleur);
		}
	}
	
	private static final long serialVersionUID = 1L;
	private ArrayList<Point> points1 = new ArrayList<Point>();
//	private ArrayList<Point> points2 = new ArrayList<Point>();
	private ArrayList<Hyperbola> hyperboles = new ArrayList<Hyperbola>();
	
	private boolean afficheFond;
	private int sizeX = 900, sizeY = 600; // taille par défaut
	private Image image;
	
	/**
	 * Crée un affichage. Le paramètre contrôle l'utilisation du fichier "fond.png" comme image de fond.
	 * @param afficheFond
	 */
	public Display(boolean afficheFond)
	{
		this.afficheFond = afficheFond;
		if(afficheFond)
		{
			try {
				image = ImageIO.read(new File("fond.png"));
			} catch (IOException e) {
				this.afficheFond = false;
				System.out.println("Fichier fond.png introuvable !");
			}
			sizeX = image.getWidth(this);
			sizeY = image.getHeight(this);
		}
		showOnFrame();
	}	
	
	// Conversions qui pourront être utiles un jour
/*	private int distanceXtoWindow(int dist)
	{
		return dist*sizeX/3000;
	}

	private int distanceYtoWindow(int dist)
	{
		return dist*sizeY/2000;
	}

	private int WindowToX(int x)
	{
		return x*3000/sizeX-1500;
	}

	private int WindowToY(int y)
	{
		return 2000-y*2000/sizeY;
	}
*/

	private int XtoWindow(double x)
	{
		return (int)((x+1500)*sizeX/3000);
	}

	private int YtoWindow(double y)
	{
		return (int)((2000-y)*sizeY/2000);
	}
	
	/**
	 * Appelé automatiquement. Affiche tous les points
	 */
	public synchronized void paint(Graphics g)
	{
		g.setColor(Color.WHITE);
		if(afficheFond)
			g.drawImage(image, 0, 0, this);
		else
			g.fillRect(0, 0, sizeX, sizeY);

		for(Hyperbola h : hyperboles)
		{
			drawHyperbola(g, h);
		}

		Point last = null;
		for(Point p : points1)
		{
			drawPoint(g, p, 8);
			if(last != null)
				drawLine(g, last, p);
			last = p;
		}
		
/*		last = null;
		for(Point p : points2)
		{
			drawPoint(g, p, 8);
			if(last != null)
				drawLine(g, last, p);
			last = p;
		}*/
	}

	/**
	 * Affichage d'une hyperbole
	 * @param g
	 * @param h
	 */
	public void drawHyperbola(Graphics g, Hyperbola h)
	{
		double a = h.delta / 2;
		double c = h.p1.distance(h.p2) / 2;
		double b = Math.sqrt(c*c - a*a);
		Vec2 centre =  new Vec2((h.p1.x + h.p2.x) / 2, (h.p1.y + h.p2.y) / 2);
		double angle = Math.atan2(h.p2.y - h.p1.y, h.p2.x - h.p1.x);
		double cos = Math.cos(angle);
		double sin = Math.sin(angle);
		Point last = null, point;
		for(double i = -10000; i < 10000; i++)
		{
			double x = -a*Math.cosh(i/1000);
			double y = b*Math.sinh(i/1000);
			Vec2 p = new Vec2((int)(cos*x-sin*y), (int)(sin*x+cos*y));
			p.x += centre.x;
			p.y += centre.y;
			point = new Point(p, Couleur.NOIR);
			if(last != null)
				drawLine(g, last, point);
			last = point;
		}
	}
	
	/**
	 * Affiche un point à l'écran
	 * @param g
	 * @param p
	 * @param taille
	 */
	public void drawPoint(Graphics g, Point p, int taille)
	{
		g.setColor(p.couleur.couleur);
		g.fillOval(XtoWindow(p.x)-taille/2,
				YtoWindow(p.y)-taille/2,
				taille,
				taille);
	}
	
	public void drawLine(Graphics g, Point p1, Point p2)
	{
		g.setColor(Color.BLACK);
		g.drawLine(XtoWindow(p1.x), YtoWindow(p1.y), XtoWindow(p2.x), YtoWindow(p2.y));
	}
	
	public void showOnFrame()
	{
		setBackground(Color.WHITE);
		setPreferredSize(new Dimension(sizeX,sizeY));
		JFrame frame = new JFrame("Balise T3");
		frame.getContentPane().add(this);
		frame.pack();
		frame.setVisible(true);
	}

	public synchronized void addPointList1(Vec2 p)
	{
		addPointList1(p, Couleur.ROUGE);
	}
	
	public synchronized void addPointList1(Vec2 p, Couleur couleur)
	{
		if(p.x >= -1500 && p.x <= 1500 && p.y >= 0 && p.y <= 2000)
		{
			points1.add(new Point(p, couleur));
			repaint();
		}
	}
/*
	public synchronized void addPointList2(Vec2 p)
	{
		if(p.x >= -1500 && p.x <= 1500 && p.y >= 0 && p.y <= 2000)
		{
			points2.add(new Point(p));
			repaint();
		}
	}*/

	public synchronized void clearPoints()
	{
		points1.clear();
//		points2.clear();
		repaint();
	}
	
	public synchronized void addHyperbola(Hyperbola h)
	{
		hyperboles.add(h);
		repaint();
	}

	public synchronized void clearHyperboles()
	{
		hyperboles.clear();
		repaint();
	}


	/**
	 * Sauvegarde (en png) l'image
	 * @param filename
	 */
	public void saveImage(String filename)
	{
		BufferedImage bi = new BufferedImage(sizeX, sizeY, BufferedImage.TYPE_INT_RGB);
		paint(bi.getGraphics());
	    try {
			ImageIO.write(bi, "PNG", new File(filename));
		} catch (IOException e) {
			System.err.println(e);
		}
	}
	
}
