package com.example.plagiomusicale;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.List;

public class CustomAdapter extends ArrayAdapter<Case> {
    private LayoutInflater inflater;

    public CustomAdapter(Context context, int resourceId, List<Case> objects) {
        super(context, resourceId, objects);
        inflater = LayoutInflater.from(context);
    }

    public View getView(int position, View v, ViewGroup parent) {
        if (v == null) {
            v = inflater.inflate(R.layout.case_list_element, null);
        }

        Case c = getItem(position);

        TextView firstArtist;
        TextView secondArtist;
        TextView first_song;
        TextView second_song;
        TextView date_posed;
        ImageView fotoPlagio1;
        ImageView fotoPlagio2;

        fotoPlagio1 = (ImageView) v.findViewById(R.id.fotoplagio1);
        fotoPlagio2 = (ImageView) v.findViewById(R.id.fotoplagio2);
        firstArtist = (TextView) v.findViewById(R.id.caso1);
        secondArtist = (TextView) v.findViewById(R.id.caso2);
        first_song = (TextView) v.findViewById(R.id.song1);
        second_song = (TextView) v.findViewById(R.id.song2);
        date_posed = (TextView) v.findViewById(R.id.data);

        String[] artisti = c.getTitle().split(" vs ");
        String dataCut = c.getDate_posted().substring(5,16);
        firstArtist.setText(artisti[0]);
        secondArtist.setText(artisti[1]);
        first_song.setText(c.getFirst_song());
        second_song.setText(c.getSecond_song());
        date_posed.setText(dataCut);
        if(c.getIs_plagiarism())
            fotoPlagio2.setImageResource(R.drawable.plagiarism);
        else
            fotoPlagio2.setImageResource(R.drawable.no_plagiarism);
        if(c.getHas_trial())
        {
            if(c.getHas_verdict())
            {
                fotoPlagio1.setImageResource(R.drawable.bilancia);
            }
            else
                fotoPlagio1.setImageResource(R.drawable.bilancia_grigia);
        }
        else
            fotoPlagio1.setImageResource(R.drawable.bilancia_grigia_sbarrata);

        firstArtist.setTag(position);
        secondArtist.setTag(position);
        first_song.setTag(position);
        second_song.setTag(position);
        date_posed.setTag(position);
        fotoPlagio1.setTag(position);
        fotoPlagio2.setTag(position);

        return v;
    }
}
