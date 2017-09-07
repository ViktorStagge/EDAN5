package helpers;

import java.util.Random;

public class Statistics {
	public static int[] randomSequence(int n){
		Random r = new Random();
		
		int[] p = new int[n];
		for(int i = 0; i < p.length; i++){
			p[i] = i+1;
		}
		
		for(int i = p.length; i >= 1; i--){
			int j = r.nextInt(i);
			int temp = p[i-1];
			p[i-1] = p[j];
			p[j] = temp;
		}
		
		return p;
	}
	
	public static double mean(int[] a){
		long sum = 0;
		for(int v : a){
			sum += v;
		}
		return (double) sum / a.length; 
	}
	
	public static double std(int[] a, int ddof){
		double mean = mean(a);
		double sum = 0;
		for(int v : a){
			sum += (v-mean)*(v-mean);
		}
		return Math.sqrt(sum/(a.length - ddof));
	}
}
