package balise;

/**
 * Utilisé pour le debug
 * @author pf
 *
 */

public class Debug {

	public static void main(String[] args)
	{
		Point simul = new Point(100, 400);
		
		int t0 = (int)simul.distance(new Point(-1500, 0));
		int t1 = (int)simul.distance(new Point(-1500, 2000));
		int t2 = (int)simul.distance(new Point(1500, 1000));
		
    	System.out.println(t0+" "+t1+" "+t2);
		Triangulation.computePoints((int)(t0 / 0.34), (int)(t1 / 0.34), (int)(t2 / 0.34));
	}

}
