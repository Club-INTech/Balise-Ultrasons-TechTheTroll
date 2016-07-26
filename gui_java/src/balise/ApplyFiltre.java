package balise;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;

import filtres.Filtre;
import filtres.FiltreMediane;
import filtres.Vec2;

/**
 * Filtre une trajectoire
 * @author pf
 *
 */

public class ApplyFiltre
{

	public static void main(String[] args)
	{
		args = new String[2];
		args[0] = "../Benchmark/Test acquisition vanilla-chocolate.txt";
		args[1] = "../Benchmark/out-filtre.txt";

		if(args.length < 1)
		{
			System.out.println("Utilisation : java -jar applyfiltre.jar input-file output-file");
			System.out.println("Le fichier d'entrée doit être au format vanille-chocolat.");
			return;
		}
			
		Filtre filtre = new FiltreMediane();
		FileProcess input = new FileProcess();
		BufferedWriter output;
		
		try {
			input.open(args[0]);
			output = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(args[1]), "utf-8"));

			double[] temps;

			while(true)
			{
				temps = input.getTemps();
	
				if(temps == null)
					break;

				Vec2 out = filtre.filtre(temps[0], temps[1], temps[2], Triangulation.computePoints(temps[0], temps[1], temps[2]));
				output.write((int)out.x+"\t"+(int)out.y+"\n");
			}
			System.out.println("Done.");
			input.close();
			output.close();
		} catch (IOException e1) {
			System.out.println(e1);
		}
	}
}
