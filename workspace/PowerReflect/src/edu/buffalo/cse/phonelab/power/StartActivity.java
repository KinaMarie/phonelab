package edu.buffalo.cse.phonelab.power;

import java.util.List;

import android.location.LocationManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.wifi.WifiConfiguration;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Debug.MemoryInfo;
import android.annotation.TargetApi;
import android.app.Activity;
import android.app.ActivityManager;
import android.app.ActivityManager.RunningAppProcessInfo;
import android.content.Intent;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

@TargetApi(16)
public class StartActivity extends Activity {

	private Button btnStart;
	private Button btnStop;
	private Button btnActivity;
	private Button btnConnectivity;
	private Button btnWifi;
	private ActivityManager mActivity;
	ActivityManager.MemoryInfo mInfo;
	ConnectivityManager mConnectivity;
	WifiManager mWifi;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_start);
        
        mInfo = new ActivityManager.MemoryInfo ();
        mActivity = (ActivityManager) this.getSystemService( ACTIVITY_SERVICE );
        mConnectivity = (ConnectivityManager)this.getSystemService(CONNECTIVITY_SERVICE);
        mWifi = (WifiManager)this.getSystemService(WIFI_SERVICE);
        btnStart = (Button)findViewById(R.id.start);
        btnStop = (Button)findViewById(R.id.stop);
        btnActivity = (Button)findViewById(R.id.btActivity);
        btnConnectivity = (Button)findViewById(R.id.btConnectivity);
        btnWifi = (Button)findViewById(R.id.btWifi);
        final Intent myIntent = new Intent(this, TestIntentService.class);
       
        btnStart.setOnClickListener(new OnClickListener()
        {

			@Override
			public void onClick(View v) {
				Log.i("TAG", "Start Button Clicked");
				startService(myIntent);
				
			}
        	
        });
        
        btnStop.setOnClickListener(new OnClickListener()
        {

			@Override
			public void onClick(View v) {
				Log.i("TAG", "Stop Button Clicked");
				stopService(myIntent);
				
			}
        	
        });
        
        
        btnActivity.setOnClickListener( new OnClickListener()
        {
        	public void onClick(View v){
        		Log.i("RawActivityManager", "Get Activity Button Clicked");
        		getActivityData();
        	}
        });
        
        
        btnConnectivity.setOnClickListener( new OnClickListener()
        {
        	public void onClick(View v){
        		Log.i("RawConnectivityManager", "Get Connectivity Button Clicked");
        		getConnectivityData();
        	}
        });
        
        btnWifi.setOnClickListener( new OnClickListener()
        {
        	public void onClick(View v){
        		Log.i("RawWifiManager", "Get Wifi Button Clicked");
        		getWifiData();
        	}
        });
    }
    
    public void getActivityData()
    {
    	List<ActivityManager.RunningAppProcessInfo> mRunningProcessList = mActivity.getRunningAppProcesses();
    	int len = mRunningProcessList.size();
    	int[] pidList = new int[len];
    	for(int i = 0; i < mRunningProcessList.size(); i++ )
    	{
    		Log.i("RunningProcessList",mRunningProcessList.get(i).uid + " "+ mRunningProcessList.get(i).pid +" "+mRunningProcessList.get(i).processName);
    		pidList[i] = mRunningProcessList.get(i).pid;
    	}
    	
    	mActivity.getMemoryInfo( mInfo );
    	Log.i("MemoryInfo", "Available Memory: "+mInfo.availMem+" Total Memeory Accessible: "+mInfo.totalMem+" Threshold Level: "+mInfo.threshold+" Low on memory? "+mInfo.lowMemory);
    	Log.i("DalvikMemInfo","Private dirty pages: "+(new MemoryInfo()).dalvikPrivateDirty+" Shared dirty pages: "+(new MemoryInfo()).dalvikSharedDirty);
    	
    	MemoryInfo[] mInfoList = mActivity.getProcessMemoryInfo(pidList) ;
    	for(int i = 0;i < mInfoList.length ; i++)
    	{
    		Log.i("ProcessMemoryInfo","Pid: "+pidList[i]+" Total Shared Dirty :"+mInfoList[i].getTotalSharedDirty()+ " Total Private Dirty: "+ mInfoList[i].getTotalPrivateDirty()+ " Total Pss: "+ mInfoList[i].getTotalPss());
    	}
    	
    	List<ActivityManager.RunningServiceInfo> mRunningServiceList = mActivity.getRunningServices(25);
    	for(int i = 0; i < mRunningServiceList.size();i++)
    	{
    		Log.i("RunningServiceList", "uid: "+mRunningServiceList.get(i).uid+" pid: "+mRunningServiceList.get(i).pid+" activeSince: "+mRunningServiceList.get(i).activeSince+" service: "+mRunningServiceList.get(i).service.toString());
    	}
    
    }
    
    public void getConnectivityData()
    {
    	NetworkInfo[] mNetworkList = mConnectivity.getAllNetworkInfo();
    	NetworkInfo active = mConnectivity.getActiveNetworkInfo();
    	Log.i("ConnectivityInfo:", "Network Preference: "+mConnectivity.getNetworkPreference());
    	Log.i("ConnectivityInfo: ","Active Network : "+active.getTypeName()+" : "+active.getExtraInfo());
    	for(int i=0;i<mNetworkList.length;i++)
    	{
    		Log.i("ConnectivityInfo",mNetworkList[i].getTypeName()+":"+mNetworkList[i].getType()+" : "+mNetworkList[i].getExtraInfo());
    	}
    	
    }
    
    public void getWifiData()
    {
    	List<WifiConfiguration> mConfigList = mWifi.getConfiguredNetworks();
    	for(int i=0;i < mConfigList.size(); i++)
    	{
    		Log.i("WifiNetworkList","SSID: "+mConfigList.get(i).SSID+" BSSID: "+mConfigList.get(i).BSSID+" Priority: "+mConfigList.get(i).priority +" Status: "+mConfigList.get(i).status + " hiddenSSID: "+mConfigList.get(i).hiddenSSID);
    	}
    	Log.i("CurrentWifiInfo","SSID: "+mWifi.getConnectionInfo().getSSID()+" BSSID: "+mWifi.getConnectionInfo().getBSSID()+" MacAddr: "+mWifi.getConnectionInfo().getMacAddress()+" LinkSpeed: "+mWifi.getConnectionInfo().getLinkSpeed()+" Rssi: "+mWifi.getConnectionInfo().getRssi());
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_start, menu);
        return true;
    }
}
