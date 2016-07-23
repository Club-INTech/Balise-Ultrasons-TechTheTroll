package balise;

import balise.Point;

/**
 * Fichier à lancer pour faire des tests balises
 * @author pf
 *
 */

public class TestBalise {

	public static void main(String[] args)
	{
		Display display = new Display(false);
		Triangulation.computePoints(192979540, 192981611, 192984391);
		display.addPoint(Triangulation.getPoint1());
		display.addPoint(Triangulation.getPoint2());
		
		while(true)
		{
			try {
				Thread.sleep(2000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}

}
