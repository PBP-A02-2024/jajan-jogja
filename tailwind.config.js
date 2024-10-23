// import colors from 'tailwindcss/colors'

export const theme = {
    extend:{
        colors: {
            black: '#0F0401',
            orange: '#E43D12',
            darkOrange: '#7C1D05',
            darkPink: '#D6536D',
            white: '#EBE9E1',
            darkYellow: '#C98809',
            yellow: '#EFB11D',
            lightPink: '#FFA2B6',
            grey: '#7A7A7A'
        },
        fontFamily:{
            JockeyOne: ['"Jockey One"'],
        },
        keyframes: {
            slideDown :{
                'from' : {transform : 'translateY(-100%)'},
                'to' : {transform : 'translateY(0%)'}
            },
            slideUp :{
                'from' : {transform : 'translateY(0%)'},
                'to' : {transform : 'translateY(-110%)'}
            }
        },
        animation:{
            slideDown : 'slideDown 1s ease-in-out',
            slideUp : 'slideUp 1s ease-in-out',
        }
    }

}