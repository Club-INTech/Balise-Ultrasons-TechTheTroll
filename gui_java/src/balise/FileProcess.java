package balise;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

/**
 * Lecteur de fichier
 * @author pf
 *
 */

public class FileProcess
{	
	private BufferedReader br;
	private String[] temps;
	
	public void open(String filename) throws FileNotFoundException
	{
		br = new BufferedReader(new FileReader(filename));	
	}
	
	public void close() throws IOException
	{
	    br.close();		
	}
	
	/**
	 * Lit un temps. Ignore les autres lignes
	 * Renvoie "null" si le fichier est fini
	 * @return
	 * @throws IOException
	 */
	public double[] getTemps() throws IOException
	{
		String line;
		double[] out = new double[3];
		while(true)
		{
			line = br.readLine();

			if(line == null)
				return null;
	
			temps = line.split(";");
			if(temps.length != 3)
				continue;

		    for(int i = 0; i < 3; i++)
		    {
		    	try
		    	{
		    		out[i] = Integer.parseInt(temps[i]);
		    	}
		    	catch(NumberFormatException e)
		    	{
		    		continue;
		    	}
		    }
		    break;
		}
	    return out;
	}
	
/*	public Vec2 getPoint() throws IOException
	{
		String line = br.readLine();
		if(line == null)
			return null;
		
		String[] split = line.split("\t");
		return new Vec2(Integer.parseInt(split[0]), Integer.parseInt(split[1]));
	}*/

}
