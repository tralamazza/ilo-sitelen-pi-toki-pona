#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <stdio.h>
#include <string>
#include <sstream>
#include <iostream>
#include <list>
#include <istream>
#include <string>
#include <fstream>
#include <streambuf>

#include <filesystem>


void ladeDatein(){
    std::list< std::string> datein;

    int datei_zahl=0;
    while(true){
        std::stringstream ss;
        ss << "lipu/" << datei_zahl << ".txt";
        auto s_str = ss.str();
        if (std::filesystem::exists(s_str)){
            std::cout << s_str <<" existiert.\n";

            std::ifstream t(s_str);
            std::string datei_str(
                (std::istreambuf_iterator<char>(t)),
                std::istreambuf_iterator<char>()
            );

            datein.push_back(datei_str);

            datei_zahl++;
        } else {
            std::cout << s_str <<" existiert nicht.\n";
            break;
        }
        
        std::cout << "datein.size " << datein.size() << "\n";
        

    }

}

int main(int argc, char ** argv)
{

    ladeDatein();
    exit(1);
    // variables
 
    bool quit = false;
    SDL_Event event;
 
    // init SDL
 
    SDL_Init(SDL_INIT_VIDEO);

    int fs_modus = SDL_WINDOW_FULLSCREEN;
#if defined(__x86_64__)
    fs_modus=0;
#endif
    SDL_Window * window = SDL_CreateWindow("SDL2 line drawing",
        SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 800, 480, fs_modus);


    SDL_Renderer * renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED|SDL_RENDERER_PRESENTVSYNC|SDL_RENDERER_TARGETTEXTURE);


    SDL_Texture* target = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, 200, 120);



    // SDL_RenderSetLogicalSize(renderer,200,120);
     // SDL_RenderSetScale(renderer,10,10);
    SDL_ShowCursor(SDL_DISABLE);


    //SDL_IMAGE
    int flags=IMG_INIT_PNG;
    int initted=IMG_Init(flags);
    if((initted&flags) != flags) {
        printf("IMG_Init: Failed to init required png support!\n");
        printf("IMG_Init: %s\n", IMG_GetError());
        // handle error
    }

        
    // load sample.png into image
    SDL_Surface *image;
    image=IMG_Load("mockup.png");
    if(!image) {
        printf("IMG_Load: %s\n", IMG_GetError());
        // handle error
    }
        SDL_Texture * fonttex = SDL_CreateTextureFromSurface(renderer, image);

        // handle events
    int t=0; 
    
    while (!quit)
    {
        t++;

        SDL_Delay(10);
        SDL_PollEvent(&event);
        SDL_SetRenderTarget(renderer, target);

    	int x1 = 0;
    	int y1 = 0;
    	int x2 = 0;
    	int y2 = 0;
    	bool drawing = false;

        switch (event.type)
        {
            case SDL_QUIT:
                quit = true;
                break;
            // TODO input handling code goes here
            case SDL_MOUSEBUTTONDOWN:
                switch (event.button.button)
                {
                    case SDL_BUTTON_LEFT:
                        x1 = event.motion.x;
                        y1 = event.motion.y;
                        x2 = event.motion.x;
                        y2 = event.motion.y;
                        drawing = true;
                        break;
                }
                break;
            case SDL_MOUSEBUTTONUP:
                switch (event.button.button)
                {
                    case SDL_BUTTON_LEFT:
                        drawing = false;
                        break;
                }
                break;
            case SDL_MOUSEMOTION:
                if (drawing)
                {
                    x2 = event.motion.x;
                    y2 = event.motion.y;
                }
                break;
        }  
     
        // clear window

        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // TODO rendering code goes here
        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
        if (drawing)
            SDL_RenderDrawLine(renderer, x1, y1, x2, y2);

        t=t%1000;

        for (int i=0;i<100;i+=10){
        	for (int j=0;j<100;j+=10){
        		 SDL_RenderDrawLine(renderer, t+i,j,i+10,t+j+10);
        	}
        }
        
        SDL_Rect rect;
        rect.x=10;
        rect.y=10;
        rect.w=20;
        rect.h=20;

        SDL_RenderDrawRect(renderer,&rect);
        // render window
        
        SDL_SetRenderTarget(renderer, 0);
            SDL_RenderCopy(renderer, fonttex, NULL, NULL);

            SDL_RenderPresent(renderer);
    }  
 
    // cleanup SDL

    IMG_Quit();

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
 
    return 0;
}
