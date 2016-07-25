package balise;

import filtres.Vec2;

/**
 * Utilisé pour le debug
 * @author pf
 *
 */

public class Debug {

	public static void main(String[] args)
	{
		Vec2 simul = new Vec2(100, 400);
		
		int t0 = (int)simul.distance(new Vec2(-1500, 0));
		int t1 = (int)simul.distance(new Vec2(-1500, 2000));
		int t2 = (int)simul.distance(new Vec2(1500, 1000));
		
    	System.out.println(t0+" "+t1+" "+t2);
		Triangulation.computePoints((int)(t0 / 0.34), (int)(t1 / 0.34), (int)(t2 / 0.34));
	}

}
