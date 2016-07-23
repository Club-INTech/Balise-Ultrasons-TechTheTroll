package balise;

import javax.imageio.ImageIO;
import javax.swing.*;

import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Interface graphique écrite à l'arrache
 * @author pf
 *
 */

public class Display extends JPanel {

	private static final long serialVersionUID = 1L;
	private ArrayList<Point> points = new ArrayList<Point>();
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
		if(afficheFond)
			g.drawImage(image, 0, 0, this);
		for(Point p : points)
			drawPoint(g, p, 8);
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
	
	public void showOnFrame()
	{
		setBackground(Color.WHITE);
		setPreferredSize(new Dimension(sizeX,sizeY));
		JFrame frame = new JFrame("Balise T3");
		frame.getContentPane().add(this);
		frame.pack();
		frame.setVisible(true);
	}
	
	public synchronized void addPoint(Point p)
	{
		points.add(p);
		repaint();
	}
	
	public synchronized void clearPoints()
	{
		points.clear();
		repaint();
	}
	
}
