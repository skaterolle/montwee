export class tweet {
    _id?: string;
    created_at?: string ;
    id?: number ;
    id_str?: string ;
    text?: string ;
    source?: string ;
    truncated?: boolean ;
    in_reply_to_status_id?: any; 
    in_reply_to_status_id_str?: any; 
    in_reply_to_user_id?: any; 
    in_reply_to_user_id_str?: any; 
    in_reply_to_screen_name?: any; 
    user?:[] ;
    geo?: [
        coordinates?: [
            first?: number,
            second?: number
        ],
    ]; 
    coordinates?: any; 
    place?: any; 
    contributors?: any; 
    retweeted_status?: [] ;
    quoted_status_id?: number ;
    quoted_status_id_str?: string ;
    quoted_status?: [] 
    quoted_status_permalink?: [] ;
    is_quote_status?: boolean ;
    quote_count?: number ;
    reply_count?: number ;
    retweet_count?: number ;
    favorite_count?: number ;
    entities?: [] ;
    extended_entities?: [] ;
    favorited?: boolean ;
    retweeted?: boolean ;
    possibly_sensitive?: boolean ;
    filter_level?: string ;
    lang?: string ;
    timestamp_ms?: string ;
}