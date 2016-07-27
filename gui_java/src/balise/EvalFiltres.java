package balise;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import filtres.Vec2;

/**
 * Test des filtres
 * @author pf
 *
 */

public class EvalFiltres
{
	public static void main(String[] args)
	{
/*
		args = new String[1];
		args[0] = "../Benchmark/out-filtre.txt";
	*/
		if(args.length < 1)
		{
			System.out.println("Utilisation : java -jar eval_filtres.jar [-background] input-file-1 [input-file-2 …]");
			return;
		}
		
		int indexInitial = 0;
		
		boolean fond = args[0].trim().equals("-background");
		if(fond)
			indexInitial++;
		
		int nbFiltres = args.length - indexInitial;
		Display display = new Display(fond);

		BufferedReader[] br = new BufferedReader[nbFiltres];
		
		try {
			for(int i = 0; i < nbFiltres; i++)
				br[i] = new BufferedReader(new FileReader(args[i+indexInitial]));
		} catch (FileNotFoundException e) {
			System.out.println(e);
		}

		try {
			int non;
			do
			{
				non = 0;
				for(int i = 0; i < nbFiltres; i++)
				{
					String line = br[i].readLine();
					if(line == null)
					{
						non++;
						continue;
					}
					String[] tmp = line.split("\t");					
					display.addPoint(new Vec2(Integer.parseInt(tmp[0]), Integer.parseInt(tmp[1])), i);
				}
			} while(non < nbFiltres);
			System.out.println("Tous les points sont affichés.");
			display.saveImage("eval.png");
			try {
				for(int i = 0; i < nbFiltres; i++)
					br[i].close();
			} catch (FileNotFoundException e) {
				System.out.println(e);
			}

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
