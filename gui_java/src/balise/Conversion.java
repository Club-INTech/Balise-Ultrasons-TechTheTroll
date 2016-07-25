package balise;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;

/**
 * Conversion de fichier
 * @author pf
 *
 */

public class Conversion {

	@SuppressWarnings("resource")
	public static void main(String[] args)
	{
/*		args = new String[2];
		args[0] = "../Benchmark/P1.txt";
		args[1] = "../Benchmark/test.txt";
*/
		if(args.length != 2)
		{
			System.out.println("Utilisation : java -jar conversion.jar input-file output-file");
			return;
		}
		
		BufferedReader br;
		BufferedWriter out;
		
		try {
			br = new BufferedReader(new FileReader(args[0]));
		} catch (FileNotFoundException e1) {
			System.err.println(e1);
			return;
		}
		try {
			out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(args[1]), "utf-8"));
		} catch (UnsupportedEncodingException e1) {
			System.err.println(e1);
			try {
				br.close();
			} catch (IOException e) {
				System.err.println(e);
			}
			return;
		} catch (FileNotFoundException e1) {
			System.err.println(e1);
			try {
				br.close();
			} catch (IOException e) {
				System.err.println(e);
			}
			System.err.println(e1);
			return;
		}
		try {
			out.write("# T3 patented");
			out.newLine();
			while(true)
			{
				String[] timestamps = new String[3];
				for(int i = 0; i < 3; i++)
				{
					String line = br.readLine();
					if(line == null)
					{
						out.close();
					    br.close();		
						System.out.println("Done.");
					    return;	
					}
					if(!line.contains(";") || line.split(";").length != 2)
						i--;
					else
					{
						int indice = Integer.parseInt(line.split(";")[0]);
						if(timestamps[indice] !=  null)
						{
							System.err.println("Indice en doublon : "+indice);
							return;
						}
						timestamps[indice] = line.split(";")[1];
					}
				}
				// TODO à vérifier
				out.write(timestamps[1]+";"+timestamps[0]+";"+timestamps[2]);
				out.newLine();
			}
			

		} catch (IOException e) {
			return;
		}	

	}

}
