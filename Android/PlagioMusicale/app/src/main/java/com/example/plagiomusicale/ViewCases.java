package com.example.plagiomusicale;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;

import com.fasterxml.jackson.core.JsonGenerationException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import org.jetbrains.annotations.NotNull;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.FormatFlagsConversionMismatchException;
import java.util.HashMap;
import java.util.Map;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class ViewCases extends Fragment {

    public ListView listView;
    public CustomAdapter customAdapter;
    private Button Search;
    private int click=0;
    private LinearLayout menu;
    private Button apriMenu;
    private int TopMargin=0;
    private ArrayList<Case> sentenze;
    private Case[] sentenzeArray;
    private EditText artistSearch;
    private EditText titleSearch;
    private EditText infoSearch;
    private boolean terminato;
    private String mailUser;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.view_cases, container, false);
        sentenze= new ArrayList<Case>();
        terminato=false;
        artistSearch=view.findViewById(R.id.searchArtist);
        titleSearch=view.findViewById(R.id.searchTitle);
        infoSearch=view.findViewById(R.id.searchInfo);
        listView = (ListView) view.findViewById(R.id.Cases);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Case selezionato = sentenze.get(position);
                FragmentTransaction ft =  getActivity().getSupportFragmentManager().beginTransaction();
                ft.setTransition(FragmentTransaction.TRANSIT_FRAGMENT_OPEN);
                Results fragment = new Results();
                Bundle bundle = new Bundle();
                bundle.putSerializable("selezionato", selezionato);
                fragment.setArguments(bundle);
                ft.replace(R.id.fragment_container, fragment);
                ft.addToBackStack(null);
                ft.commit();
            }
        });
        customAdapter = new CustomAdapter(getActivity(), R.layout.case_list_element, new ArrayList<Case>());
        Search=(Button) view.findViewById(R.id.search);
        apriMenu = view.findViewById(R.id.apriMenu);
        menu = (LinearLayout) view.findViewById(R.id.menuScorrevole);
        new AllCases().execute();
        apriMenu.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                if(click==0) {
                    ViewGroup.MarginLayoutParams margin= (ViewGroup.MarginLayoutParams) menu.getLayoutParams();
                    TopMargin=margin.topMargin;
                    margin.setMargins(0,-50,0,0);
                    menu.requestLayout();
                    click = 1;
                }else {
                    ViewGroup.MarginLayoutParams margin= (ViewGroup.MarginLayoutParams) menu.getLayoutParams();
                    margin.setMargins(0,TopMargin,0,0);
                    menu.requestLayout();
                    click = 0;
                }
            }
        });
        Search.setOnClickListener(new View.OnClickListener(){

            @Override
            public void onClick(View v) {
                String artist = artistSearch.getText().toString();
                String title = titleSearch.getText().toString();
                String info = infoSearch.getText().toString();
                if(artist.equals("")) artist="&";
                if(title.equals("")) title="&";
                if(info.equals("")) info="&";
                new AllCases().execute(artist,title,info);
                upSearch();
                hideSoftKeyboard(getActivity());
            }
        });
        return view;
    }


    class AllCases extends AsyncTask<String,Integer,Integer>{


        @Override
        protected Integer doInBackground(String... strings) {
            OkHttpClient client = new OkHttpClient();
            String url;
            if(strings.length==0) //Se non ci sono filtri di ricerca
                url = "http://10.0.2.2:5000/all_sentencesMobile"; //Tutti i Casi
            else //Se ci sono filtri di ricerca
                url = "http://10.0.2.2:5000/search_pageMobile?title="+strings[1]+"&author="+strings[0]+"&info="+strings[2]; //Ricerca
            Request request = new Request.Builder().url(url).build(); //Richiesta al Server
            client.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(@NotNull Call call, @NotNull IOException e) {
                    e.printStackTrace();
                }

                @Override
                public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                    String jsonStr = response.body().string(); //Scarico il JSON
                    ArrayList<HashMap<String, String>> caseList = new ArrayList<>();
                    ObjectMapper mapper = new ObjectMapper();
                    sentenzeArray = mapper.readValue(jsonStr,Case[].class); //Mappo il file JSON in un Array di Casi
                    for(int i=0;i<sentenzeArray.length;i++)
                    {
                        sentenze.add(sentenzeArray[i]);
                    }
                    terminato=true; //Comunico la fine del Download
                }
            });
            return 0;
        }

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            sentenze.clear();
            System.out.println("ELIMINO SENTENZE");
        }

       @Override
        protected void onPostExecute(Integer i) {
            super.onPostExecute(i);
            while(!terminato) {}
            System.out.println("SONO IN POST EXECUTE");
            updateGUI(sentenze);
        }
    }

    private void updateGUI(ArrayList<Case> sentenze)
    {
        customAdapter.clear();
        for(int i=0;i<sentenze.size();i++)
        {
            customAdapter.add(sentenze.get(i));
            customAdapter.notifyDataSetChanged();
        }
        customAdapter.notifyDataSetChanged();
        listView.setAdapter(customAdapter);
        terminato=false;
    }

    private void upSearch()
    {
        ViewGroup.MarginLayoutParams margin= (ViewGroup.MarginLayoutParams) menu.getLayoutParams();
        margin.setMargins(0,TopMargin,0,0);
        menu.requestLayout();
        click = 0;
    }


    public static void hideSoftKeyboard(Activity activity) {
        InputMethodManager inputMethodManager =
                (InputMethodManager) activity.getSystemService(
                        Activity.INPUT_METHOD_SERVICE);
        if(inputMethodManager.isAcceptingText()){
            inputMethodManager.hideSoftInputFromWindow(
                    activity.getCurrentFocus().getWindowToken(),
                    0
            );
        }
    }
}
