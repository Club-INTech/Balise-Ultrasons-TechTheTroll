package balise;

import java.io.IOException;
import java.util.Scanner;

import filtres.Vec2;

/**
 * Affiche les hyperboles pour un triplet de timestamp
 * @author pf
 *
 */

public class HyperbolaPrinter {

	public static void main(String[] args)
	{
		System.out.println("Utilisation : java -jar hyperbola_printer.jar [input-file] [-background]");
		System.out.println("Le fichier d'entrée doit être au format vanille-chocolat.");

		boolean background = (args.length >= 2 && args[1].trim().equals("-background")) || (args.length >= 1 && args[0].trim().equals("-background"));
		boolean useFile = false;
		
		Display display = new Display(background);
		FileProcess file = new FileProcess();
		try {
			if((args.length == 1 && !background) || args.length > 1)
			{
				useFile = true;
				file.open(args[0]);
			}
			
			double[] temps;

			do
			{
				if(useFile)
				{
					temps = file.getTemps();	
					if(temps == null)
						break;
				}
				else
				{
					temps = new double[3];
					Scanner sc = new Scanner(System.in);
					System.out.println("Temps de réception à la balise 1 :");
					temps[0] = Integer.parseInt(sc.nextLine());
					System.out.println("Temps de réception à la balise 2 :");
					temps[1] = Integer.parseInt(sc.nextLine());
					System.out.println("Temps de réception à la balise 3 :");
					temps[2] = Integer.parseInt(sc.nextLine());
					sc.close();
					
/*		Vec2 simul = new Vec2(-1200, 500);
		
		temps[0] = 1000 + (int)(simul.distance(new Vec2(-1500, 0)) / 0.34);
		temps[1] = 1000 + (int)(simul.distance(new Vec2(-1500, 2000)) / 0.34);
		temps[2] = 1000 + (int)(simul.distance(new Vec2(1500, 1000)) / 0.34);
		
		System.out.println(temps[0]+" "+temps[1]+" "+temps[2]);*/
				}

				display.addHyperbola(new Hyperbola(0, temps[2] - temps[1]));
				display.addHyperbola(new Hyperbola(1, temps[2] - temps[0]));
				display.addHyperbola(new Hyperbola(2, temps[1] - temps[0]));

				display.addPointList1(Triangulation.computePoints(temps[0], temps[1], temps[2]));

				if(useFile)
				{
					try {
						Thread.sleep(20);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					display.clearHyperboles();
					display.clearPoints();
				}
				else
				{
					display.saveImage("test.png");
				}
			} while(useFile);
			
			if(useFile)
			{
				System.out.println("Fini.");
				file.close();
			}
			
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
