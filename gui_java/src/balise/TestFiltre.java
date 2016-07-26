package balise;

import java.io.IOException;

import filtres.Filtre;
import filtres.FiltreMediane;
import filtres.Vec2;

/**
 * Test des filtres
 * @author pf
 *
 */

public class TestFiltre
{
	public static void main(String[] args)
	{
/*
		args = new String[1];
		args[0] = "../Benchmark/Test acquisition vanilla-chocolate.txt";
	*/	
		if(args.length < 1)
		{
			System.out.println("Utilisation : java -jar testbalise.jar input-file [-background]");
			System.out.println("Le fichier d'entrée doit être au format vanille-chocolat.");
			return;
		}
			
		Filtre filtre = new FiltreMediane();
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
				Vec2 solution = Triangulation.computePoints(temps[0], temps[1], temps[2]);
				display.addPoint(solution, 0);
				System.out.println(solution);
				display.addPoint(filtre.filtre(temps[0], temps[1], temps[2], solution), 1);
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

		
/*		Vec2 p1 = new Vec2(200, 1200);
		Vec2 p2 = new Vec2(300, 1100);
		Vec2 p3 = new Vec2(400, 1200);
		Vec2 p4 = new Vec2(500, 1400);
		Display display = new Display(false);
		FiltreMediane m = new FiltreMediane();
		m.giveDisplay(display);
		display.addPointList1(p1);
		display.addPointList1(m.filtre(0, 0, 0, p1), Couleur.BLEU);
		display.addPointList1(p2);
		display.addPointList1(m.filtre(0, 0, 0, p2), Couleur.BLEU);
		display.addPointList1(p3);
		display.addPointList1(m.filtre(0, 0, 0, p3), Couleur.BLEU);
		display.addPointList1(p4);
		display.addPointList1(m.filtre(0, 0, 0, p4), Couleur.BLEU);*/
	}
}
