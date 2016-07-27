package balise;

import java.awt.Color;

/**
 * Définition de quelques couleurs
 * @author pf
 *
 */
public enum Couleur
{

	BLANC(255, 255, 255),
	NOIR(0, 0, 0),
	BLEU(0, 0, 200),
	JAUNE(200, 200, 0),
	ROUGE(200, 0, 0),
	VERT(0, 200, 0),
	VIOLET(200, 0, 200);
	
	private static final int alpha = 150;
	public final Color couleur;
	
	private Couleur(int r, int g, int b, int a)
	{
		this.couleur = new Color(r,g,b,a);
	}

	private Couleur(int r, int g, int b)
	{
		this.couleur = new Color(r,g,b,alpha);
	}
}
