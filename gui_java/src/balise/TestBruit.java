package balise;

import java.util.Random;

/**
 * Test sur l'influence du bruit
 * @author pf
 *
 */

public class TestBruit {

	public static void main(String[] args)
	{
		Display display = new Display(true);
		double[] temps = new double[3];
		Random r = new Random();
		double ecartType = 100;
		for(int i = 0; i < 1000; i++)
		{
			temps[0] = 1000 + r.nextGaussian()*ecartType;
			temps[1] = 2300 + r.nextGaussian()*ecartType;
			temps[2] = 0 + r.nextGaussian()*ecartType;
			display.addPoint(Triangulation.computePoints(temps[0], temps[1], temps[2]), 1);
		}
		display.saveImage("test_bruit"+ecartType+".png");

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
