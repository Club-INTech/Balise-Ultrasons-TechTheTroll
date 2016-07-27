package filtres;

/**
 * Filtre qui lisse avec une médiane
 * @author pf
 *
 */

public class FiltreMediane implements Filtre
{
	/**
	 * Le point médian M d'un ensemble S est celui tel que:
	 * la somme des vecteurs ME/||ME|| pour tout E appartenant à S est nul.
	 */
	
	private final static int tailleMemoire = 50;
	private Vec2[] memoire = new Vec2[tailleMemoire];
	private int indice = 0;
	private boolean tour = false;
	
	@Override
	public void init(double deltaTemps)
	{
	}

	@Override
	public Vec2 filtre(double t1, double t2, double t3, Vec2 positionBrute)
	{
		memoire[indice] = positionBrute;		
		
		Vec2 sum = new Vec2();
		Vec2 m;

		if(tour)
		{
			m = new Vec2();
			for(int j = 0; j < tailleMemoire; j++)
				Vec2.plus(m, memoire[j]);
			Vec2.scalar(m, 1/tailleMemoire);
			
			int nb = 0;
			do
			{
				sum.x = 0;
				sum.y = 0;
				for(int j = 0; j < tailleMemoire; j++)
				{
					Vec2.plus(sum, memoire[j].minusNewVector(m).normalize());
				}
	
				Vec2.plus(m, sum.scalarNewVector(0.1));
				nb++;
			} while(sum.length() > 0.1 && nb < 1000);
		}
		else
			m = new Vec2(positionBrute);
		
		indice++;
		indice %= tailleMemoire;

		if(indice == 0)
			tour = true;
		
		return m;

	}
	
}
