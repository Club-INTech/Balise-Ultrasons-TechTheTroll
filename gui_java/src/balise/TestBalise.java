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
		/*
		args = new String[1];
		args[0] = "../Benchmark/P2_vanille-chocolat.txt";
*/
		
		if(args.length < 1)
		{
			System.out.println("Utilisation : java -jar testbalise.jar input-file [-background]");
			System.out.println("Le fichier d'entrée doit être au format vanille-chocolat.");
			return;
		}
			
		Display display = new Display(args.length >= 2 && args[1].trim().equals("-background"));
		FileProcess file = new FileProcess();
		try {
			file.open(args[0]);
			double[] temps;

//			for(int i = 0; i < 2; i++)
			while(true)
			{
				temps = file.getTemps();
				if(temps == null)
					break;
				display.addPointList1(Triangulation.computePoints(temps[0], temps[1], temps[2]));
			}
			System.out.println("Tous les points sont affichés.");
			display.saveImage("test.png");
			file.close();
		} catch (IOException e1) {
			System.out.println(e1);
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
