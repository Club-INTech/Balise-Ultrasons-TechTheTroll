package balise;

import java.io.IOException;

/**
 * Affiche les hyperboles pour un triplet de timestamp
 * @author pf
 *
 */

public class HyperbolaPrinter {

	public static void main(String[] args)
	{
		Display display = new Display(false);
		FileProcess file = new FileProcess();
		try {
			file.open("../Benchmark/out.txt");
			int[] temps;

			while(true)
			{
				temps = file.getTemps();
	
				if(temps == null)
					break;

//				System.out.println(temps[1] - temps[0]);
				display.addHyperbola(new Hyperbola(0, temps[2] - temps[1]));
				display.addHyperbola(new Hyperbola(1, temps[2] - temps[0]));
				display.addHyperbola(new Hyperbola(2, temps[1] - temps[0]));

				Triangulation.computePoints(temps[0], temps[1], temps[2]);
				display.addPointList1(Triangulation.getPoint1());
				
				System.out.println(Triangulation.getPoint1());
//				display.saveImage("test.png");
				
				try {
					Thread.sleep(20);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				display.clearHyperboles();
				display.clearPoints();
			}
			System.out.println("Fini.");
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
