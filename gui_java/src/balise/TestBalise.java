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
		Display display = new Display(true);
		FileProcess file = new FileProcess();
		try {
			file.open("../Benchmark/out.txt");
			int[] temps;

//			for(int i = 0; i < 2; i++)
			while(true)
			{
				temps = file.getTemps();
				if(temps == null)
					break;
				Triangulation.computePoints(temps[0], temps[1], temps[2]);
				display.addPointList1(Triangulation.getPoint1());
			}
			System.out.println("Tous les points sont affichés.");
			display.saveImage("test.png");
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
