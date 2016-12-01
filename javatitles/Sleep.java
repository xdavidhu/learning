package tk.ckdeveloper.javatitles;

public class Sleep {

	public static void sleep(int t) {
		try {
		Thread.sleep(t);
		} catch (InterruptedException e) {
		e.printStackTrace();
		}
	}
	
	
}
