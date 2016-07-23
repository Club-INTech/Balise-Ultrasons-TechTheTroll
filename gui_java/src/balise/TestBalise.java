package balise;

import java.io.IOException;

/**
 * Fichier à lancer pour faire des tests balises
 * @author pf
 *
 */

public class TestBalise {

	public static void main(String[] args)
	{
		Display display = new Display(false);
		FileProcess file = new FileProcess();
		try {
			file.open("../Benchmark/Test acquisition vanilla-chocolate.txt");
			int[] temps;

			while(true)
			{
				try {
					Thread.sleep(100);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				temps = file.getTemps();
				if(temps == null)
					break;
				Triangulation.computePoints(temps[0], temps[1], temps[2]);
				display.addPoint(Triangulation.getPoint1());
				display.addPoint(Triangulation.getPoint2());
			}

			file.close();
		} catch (IOException e1) {
			e1.printStackTrace();
		}
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
