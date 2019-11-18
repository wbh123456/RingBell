package test;

import java.io.IOException;
import java.util.concurrent.ExecutionException;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.*;


public class test {
	
	public static void main (String[] args) throws IOException, ExecutionException, InterruptedException {
		
		System.setProperty("webdriver.chrome.driver", "./chromedriver.exe");
		
		double c = 1;
		while (c < 2) {
			
			double start_time = System.currentTimeMillis();
			
			WebDriver driver = new ChromeDriver();
	
			driver.get("https://www.askform.cn/login");
			// System.out.println("URL: " + driver.getCurrentUrl());
			
			// Login
			driver.findElement(By.id("un")).sendKeys("contact.listener@gmail.com");
			driver.findElement(By.id("pwd")).sendKeys("iamyourlistener");
			driver.findElement(By.xpath(".//a[@onclick='askformLogin()']")).click();
			
			// --> 在线表单
			driver.findElement(By.id("menu4603080002")).click();
			// <li id="menu4603080002" class="active">
	        // <a href="/Survey/ApplicationIndex.aspx?AppConfigID=4603080002">
	        //  在线表单<span class="selected"> </span></a> </li>
			
			// --> find the form
			// driver.findElement(By.xpath(".//a[@class='dropdown-toggle']")).click();
			driver.findElement(By.linkText("4.管理数据")).click();
			// <a class="dropdown-toggle" aria-expanded="true" 
			// href="/Survey/DataList.aspx?AppConfigID=4603080002&amp;FormApplicationID=8194230001&amp;FormCategoryID=8224980001&amp;FormID=8604550001">
			// <i class="fa fa-database"></i><span>4.管理数据<i class="fa fa-long-arrow-right"></i></span></a>
			
			// --> get the form
			driver.findElement(By.xpath(".//input[@name='ctl00$MainContent$btnExport']")).click();
			// <input type="submit" name="ctl00$MainContent$btnExport" value="导出数据" id="btnExport" class="btn blue">
			
			// Downloading...
			Thread.sleep(10000);
			driver.quit();
			
			// Calculate time needed to get the forms
			double end_time = System.currentTimeMillis();
			double time = end_time - start_time;
			System.out.println("Time: " + Double.toString(time/1000) + "s");
			System.out.println("Count: " + Double.toString(c));
			
			c += 1;
		}
		
	}
	
}
