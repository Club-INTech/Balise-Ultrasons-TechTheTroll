package filtres;

/**
 * Classe de calcul de vecteurs de dimension 2
 * @author pf
 *
 */

public class Vec2
{
	public volatile double x;
	public volatile double y;
	
	public Vec2()
	{
		x = 0;
		y = 0;
	}
	
	public Vec2(double angle)
	{
		x = Math.cos(angle);	
		y = Math.sin(angle);
	}

	public Vec2(double longueur, double angle, boolean useless)
	{
		x = Math.cos(angle)*longueur;
		y = Math.sin(angle)*longueur;
	}

	public Vec2(Vec2 model)
	{
		x = model.x;
		y = model.y;
	}

	public Vec2(double requestedX, double requestedY)
	{
		x = requestedX;
		y = requestedY;
	}
	
	public final static Vec2 setAngle(Vec2 out, double angle)
	{
		out.x = Math.cos(angle);
		out.y = Math.sin(angle);
		return out;
	}

	// Do not square a length, use squared length directly
	// to increase performances
	public final double squaredLength()
	{
		return x*x + y*y;
	}

	// Returns this vec2's magnitude
	public final double length()
	{
		return Math.hypot(x, y);
	}
	
	// dot product
	public final double dot(Vec2 other)
	{
		return x*other.x + y*other.y;
	}

	// build a new Vec2 by summing the calling Vec2 and the one in args
	public final Vec2 plusNewVector(Vec2 other)
	{
		return new Vec2(x + other.x, y + other.y);
	}
	
	// build a new Vec2 with the value obtained by decrementing the
	// calling Vec2 by the provided Vec2 in args
	public final Vec2 minusNewVector(Vec2 other)
	{
		return new Vec2(x - other.x, y - other.y);
	}

	public final static Vec2 plus(Vec2 modified, Vec2 other)
	{
		modified.x += other.x;
		modified.y += other.y;
		return modified;
	}
	
	public final static Vec2 minus(Vec2 modified, Vec2 other)
	{
		modified.x -= other.x;
		modified.y -= other.y;
		return modified;
	}

	public final Vec2 clone()
	{
		return new Vec2(this.x, this.y);
	}

	public final double squaredDistance(Vec2 other)
	{
		double tmp_x = x-other.x, tmp_y = y-other.y;
		return tmp_x*tmp_x + tmp_y*tmp_y;
	}

	public final double distance(Vec2 other)
	{
		return Math.hypot(x-other.x, y-other.y);
	}

	public final double distanceManhattan(Vec2 other)
	{
		return Math.abs(x - other.x) + Math.abs(y - other.y);
	}

	public final String toString()
	{
		return "("+x+","+y+")";
	}
	
	public final boolean equals(Vec2 other)
	{
		return x == other.x && y == other.y;
	}

	@Override
	public final boolean equals(Object obj) {
		if (this == obj)
			return true;
		else if (obj == null)
			return false;
		else if (!(obj instanceof Vec2))
			return false;
		Vec2 other = (Vec2) obj;
		if (x != other.x || (y != other.y))
			return false;
		return true;
	}

	/**
	 * Copie this dans other.
	 * @param other
	 */
	public static final void copy(Vec2 v, Vec2 other)
	{
	    other.x = v.x;
	    other.y = v.y;
	}

	public final Vec2 middleNewVector(Vec2 b)
	{
		return new Vec2((x+b.x)/2, (y+b.y)/2);
	}

	public static final Vec2 scalar(Vec2 v, double d)
	{
		v.x = d*v.x;
		v.y = d*v.y;
		return v;
	}

	public static final Vec2 Ysym(Vec2 v, boolean symetrie)
	{
		if(symetrie)
			v.y = -v.y;
		return v;
	}

	public final Vec2 scalarNewVector(double d)
	{
		Vec2 out = new Vec2(this);
		scalar(out, d);
		return out;
	}
	
	public final Vec2 rotateNewVector(double angle, Vec2 centreRotation)
	{
		double cos = Math.cos(angle);
		double sin = Math.sin(angle);
		return new Vec2(cos*(x-centreRotation.x)-sin*(y-centreRotation.y)+centreRotation.x,
		sin*(x-centreRotation.x)+cos*(y-centreRotation.y)+centreRotation.y);
	}

	public final Vec2 rotateNewVector(double cos, double sin, Vec2 centreRotation)
	{
		return new Vec2(cos*(x-centreRotation.x)-sin*(y-centreRotation.y)+centreRotation.x,
		sin*(x-centreRotation.x)+cos*(y-centreRotation.y)+centreRotation.y);
	}

	public final static Vec2 rotate(Vec2 v, double cos, double sin, Vec2 centreRotation)
	{
		double a = (cos*(v.x-centreRotation.x)-sin*(v.y-centreRotation.y))+centreRotation.x;
		v.y = (sin*(v.x-centreRotation.x)+cos*(v.y-centreRotation.y))+centreRotation.y;
		v.x = a;
		return v;
	}

	/**
	 * Rotation avec pour centre de rotation (0,0)
	 * @param d
	 * @return
	 */
	public final Vec2 rotateNewVector(double angle)
	{
		double cos = Math.cos(angle);
		double sin = Math.sin(angle);
		return new Vec2(cos*x-sin*y, sin*x+cos*y);
	}

	public final static Vec2 rotate(Vec2 v, double angle)
	{
		double cos = Math.cos(angle);
		double sin = Math.sin(angle);
		double old_x = v.x;
		v.x = cos*v.x-sin*v.y;
		v.y = sin*old_x+cos*v.y;
		return v;
	}

	public final static Vec2 rotate(Vec2 v, double cos, double sin)
	{
		double old_x = v.x;
		v.x = cos*v.x-sin*v.y;
		v.y = sin*old_x+cos*v.y;
		return v;
	}

	public final double getArgument()
	{
		return Math.atan2(y, x);
	}
	
	/**
	 * Fait le projeté de this sur other, puis renvoie le résultat dans un nouveau Vec2
	 * @param other
	 * @return
	 */
	public final Vec2 projectOnNewVector(Vec2 other)
	{
		return scalarNewVector(dot(other));
	}

	/**
	 * Tourne le vecteur de PI/2
	 * @return
	 */
	public final static Vec2 rotateAngleDroit(Vec2 v)
	{
		double tmp = v.x;
		v.x = -v.y;
		v.y = tmp;
		return v;
	}

	/**
	 * v devient -v
	 * @param v
	 * @return
	 */
	public final static Vec2 oppose(Vec2 v)
	{
		v.x = -v.x;
		v.y = -v.y;
		return v;
	}

	public Vec2 normalize()
	{
		if(x == 0 && y == 0)
			return this;
		double length = length();
		x /= length;
		y /= length;
		return this;
	}
	
}

